import json
import os

from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
import boto3
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.data_classes.appsync import scalar_types_utils

# Initialize Clients
bedrock_agent_runtime_client = boto3.client(
    "bedrock-agent-runtime", region_name="us-east-1"
)
logger = Logger(service="invoke_supervisor_lambda")
tracer = Tracer(service="invoke_agent_supervisor_lambda")
agent_id = os.environ.get("AGENT_ID")
agent_alias = os.environ.get("AGENT_ALIAS")


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event, context):
    api_event = APIGatewayProxyEvent(event)

    try:
        logger.info(f"Received event: {api_event.body}")
        query  = api_event.json_body["query"]
        logger.info(f"User query {query}")

        # Validate input
        if query is None:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Bad Request: 'query' parameter is required"}),
                "headers": {
                    "Content-Type": "application/json"
                }
            }



        # Generate a unique session ID
        session_id = scalar_types_utils.make_id()



        # Invoke the Bedrock Agent
        agent_response = bedrock_agent_runtime_client.invoke_agent(
            inputText=query,
            agentId=agent_id,
            agentAliasId=agent_alias,
            sessionId=session_id,
            enableTrace=True,
        )

        # Ensure the response contains the event stream
        if "completion" not in agent_response:
            logger.error("Agent response is missing completion field.")
            return {
                "statusCode": 502,
                "body": json.dumps({"message": "Bad Gateway: Invalid response from agent"}),
                "headers": {
                    "Content-Type": "application/json"
                }
            }

        event_stream = agent_response["completion"]

        # Collect all chunks from the stream
        chunks = []
        for event in event_stream:
            chunk = event.get("chunk")
            if chunk:
                decoded_bytes = chunk.get("bytes").decode()
                logger.debug(f"Received chunk: {decoded_bytes}")
                chunks.append(decoded_bytes)
        completion = " ".join(chunks)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Success",
                "response": completion
            }),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    except Exception as e:
        logger.error(f"Unhandled error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Internal Server Error",
                "error": str(e)
            }),
            "headers": {
                "Content-Type": "application/json"
            }
        }