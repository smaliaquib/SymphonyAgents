from aws_cdk import (
    Stack,
    Duration,
    aws_apigateway as apigw,
    aws_lambda as _lambda,
    CfnOutput,
)
from aws_cdk.aws_apigateway import UsagePlanPerApiStage, UsagePlan, Stage, Deployment
from aws_cdk.aws_iam import PolicyStatement
from aws_cdk.aws_lambda import Runtime
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from constructs import Construct
from datetime import datetime, timedelta


class RestApiStack(Stack):
    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            aiAgentId: str,
            aiAgentAlias: str,

            **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        invoke_supervisor_lambda = PythonFunction(
            self,
            "InvokeSupervisorAgent",
            runtime=Runtime.PYTHON_3_11,
            entry="./lambda",
            index="invoke_supervisor_agent.py",
            handler="handler",
            timeout=Duration.minutes(4),
            memory_size=512,
        )

        invoke_supervisor_lambda.add_to_role_policy(
            PolicyStatement(
                actions=[

                    "bedrock:InvokeAgent",
                    "bedrock:InvokeModelWithResponseStream",
                ],
                resources=["*"],
                # Grant access to all Bedrock models
            )
        )

        invoke_supervisor_lambda.add_environment("AGENT_ID", aiAgentId)
        invoke_supervisor_lambda.add_environment("AGENT_ALIAS", aiAgentAlias)

        # API Gateway setup
        multi_agent_rest_api = apigw.RestApi(
            self, "MultiAgentRestApi",
            rest_api_name="multi-agent-rest-api",
            description="A Rest API that interacts securely with a multi agent ai application",

            deploy_options=apigw.StageOptions(
                throttling_rate_limit=100,
                throttling_burst_limit=200
            )
        )
        # API Key
        api_key = multi_agent_rest_api.add_api_key(
            "MultiAgentRestAPIKey",
            api_key_name="MultiAgentRestAPIKey",
            description="API Key for Secure Access"

        )

        multi_agent_rest_api_usage_plan = UsagePlan(
            self,
            "MultiAgentRestAPIKeyUsagePlan",
            name="MultiAgentRestAPIKeyUsagePlan",
            api_stages=[{
                "api": multi_agent_rest_api,
                "stage": multi_agent_rest_api.deployment_stage
            }],

            throttle=apigw.ThrottleSettings(rate_limit=50, burst_limit=100),
            quota=apigw.QuotaSettings(limit=10000, period=apigw.Period.MONTH),
        )
        multi_agent_rest_api_usage_plan.add_api_key(api_key=api_key)

        multi_agent_rest_api_resource = multi_agent_rest_api.root.add_resource("supervisor")


        multi_agent_rest_api_resource.add_method(
            "POST",
            apigw.LambdaIntegration(invoke_supervisor_lambda),

            api_key_required=True
        )


        # Outputs
        CfnOutput(self, "API URL", value=multi_agent_rest_api.url)
        CfnOutput(self, "API Key", value=api_key.key_id)
