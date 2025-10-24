from aws_cdk import (
    # Duration,
    Stack, aws_dynamodb, RemovalPolicy, aws_s3,
    # aws_sqs as sqs,
)
from aws_cdk.aws_lambda import Runtime
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from cdklabs.generative_ai_cdk_constructs.pinecone import PineconeVectorStore
from constructs import Construct

from cdklabs.generative_ai_cdk_constructs.bedrock import (
    Agent,
    AgentAlias, BedrockFoundationModel, AgentActionGroup, ActionGroupExecutor, ApiSchema, VectorKnowledgeBase,
    S3DataSource, ChunkingStrategy, AgentCollaborator, AgentCollaboratorType

)

class MultiAgentAiTutStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define the DynamoDB table

        todo_item_table = aws_dynamodb.Table(
            self,
            "TodoItemAgentTable",
            table_name="TodoItemAgentTable",
            partition_key=aws_dynamodb.Attribute(
                name="id", type=aws_dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY,

            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,

        )





        todo_agent = Agent(
            self,
            "todoAgent",
            should_prepare_agent=True,
            foundation_model=BedrockFoundationModel.ANTHROPIC_CLAUDE_3_5_SONNET_V1_0,
            instruction="You are a helpful and friendly agent that performs CRUDL operations on a dynamodb table",
        )

        todo_agent_alias = AgentAlias(
            self,
            "TodoAgentAlias",
            agent=todo_agent,
            description="Todo Alias for description"
        )

        todo_agent_item_function = PythonFunction(
                self,
                "TodoItemAgentLambdaFunction",
                runtime=Runtime.PYTHON_3_11,
                entry="./lambda",
                index="agent.py",
                handler="lambda_handler",
            )

        todo_action_group: AgentActionGroup = AgentActionGroup(
            name="TodoItemAgentActionGroup",
            description="Use these functions to create/update/Read/delete and list todo items",
            executor=ActionGroupExecutor.fromlambda_function(
                lambda_function=todo_agent_item_function,
            ),
            enabled=True,
            api_schema=ApiSchema.from_local_asset("./lambda/openapi.json"),
        )

        todo_agent.add_action_group(todo_action_group)

        todo_item_table.grant_read_write_data(todo_agent_item_function)

        todo_agent_item_function.add_environment("TODO_ITEM_TABLE",todo_item_table.table_name)

        # create an agent for the content

        # create an alias

        content_generation_agent = Agent(
            self,
            "ContentGenerationAgent",
            should_prepare_agent=True,

            foundation_model=BedrockFoundationModel.ANTHROPIC_CLAUDE_3_5_SONNET_V1_0,
            instruction="You Specialize in answering content generation questions for our workshops",
        )

        content_generation_agent_alias = AgentAlias(
            self,
            "ContentGenerationAgentAlias",
            agent=content_generation_agent,
            description="Content Generation Agent Alias for description"
        )

        faq_agent = Agent(
            self,
            "FAQAgent",
            should_prepare_agent=True,

            foundation_model=BedrockFoundationModel.ANTHROPIC_CLAUDE_3_5_SONNET_V1_0,
            instruction="You Specialize in answering customer support questions for this application",
        )

        faq_agent_alias = AgentAlias(
            self,
            "CFAQAgentAlias",
            agent=faq_agent,

            description="Frequently Asked Questions Agent Alias for description"
        )



        # create a pinecone cdk resource

        pinecone_vec = PineconeVectorStore(
            connection_string='https://ai-l,,,.........',
            credentials_secret_arn='arn:aws:secretsmanager:us-east-jkkkkkkkk.......',
            text_field='text',
            metadata_field='metadata'
        )
        # Create vectorknowdledge store

        kb = VectorKnowledgeBase(self, 'ContentAgentKnowledgeBase',
                                 name="ContentAgentKnowledgeBase",

                                 vector_store=pinecone_vec,
                                 embeddings_model=BedrockFoundationModel.TITAN_EMBED_TEXT_V2_1024,
                                 instruction='Use this knowledge base to summarize,generate QA and flash cards about workshops ' +
                                             'It contains some workshops gotten from educloud.academy.'
                                 )

        faq_kb = VectorKnowledgeBase(self, 'FAQAgentKnowledgeBase',
                                     name="FAQAgentKnowledgeBase",
                                     vector_store=pinecone_vec,
                                     embeddings_model=BedrockFoundationModel.TITAN_EMBED_TEXT_V2_1024,
                                     instruction='Use this knowledge base to answer all customer support queries.'
                                     )

        # create s3 bucket and assign the bucket as a datasource to our knowledge base

        docBucket = aws_s3.Bucket(
            self,
            "ai-learning-bucket",
            versioned=False,
            encryption=aws_s3.BucketEncryption.S3_MANAGED,
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
        )

        S3DataSource(self, 'DataSource',
                     bucket=docBucket,
                     knowledge_base=kb,
                     data_source_name='ai-todo-workshops',
                     chunking_strategy=ChunkingStrategy.FIXED_SIZE,
                     )

        faqBucket = aws_s3.Bucket(
            self,
            "faq-bucket",
            versioned=False,
            encryption=aws_s3.BucketEncryption.S3_MANAGED,
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
        )

        S3DataSource(self, 'FAQDataSource',
                     bucket=faqBucket,
                     knowledge_base=faq_kb,
                     data_source_name='faq-datasource',
                     chunking_strategy=ChunkingStrategy.FIXED_SIZE,
                     )

        faq_agent.add_knowledge_base(faq_kb)
        content_generation_agent.add_knowledge_base(kb)

        self.supervisor_agent = Agent(
            self,
            "SuperVisorAgent",
            should_prepare_agent=True,
            foundation_model=BedrockFoundationModel.ANTHROPIC_CLAUDE_3_5_SONNET_V1_0,
            instruction=(
                "You are a helpful and friendly supervisor agent that routes user queries to the appropriate specialized agents. "
                "Analyze the user's request carefully and determine the most suitable agent based on the following roles: "
                "(1) Route questions regarding todo item management (create, read, update, delete, list tasks) to the TodoAgent. "
                "(2) Route customer support related questions, such as troubleshooting or workshop inquiries, to the CustomerSupportAgent. "
                "(3) Route content generation requests like creating summaries, workshop flashcards, or general content-related questions to the ContentGenerationAgent. "
                "If the user's query doesn't fit into any specialized category, you may provide general assistance directly."
            ),
            agent_collaboration=AgentCollaboratorType.SUPERVISOR,
            agent_collaborators=[
                AgentCollaborator(
                    agent_alias=todo_agent_alias,
                    collaborator_name="TodoAgent",
                    collaboration_instruction="Route Todo questions to this agent",
                    relay_conversation_history=True

                ),
                AgentCollaborator(
                    agent_alias=faq_agent_alias,
                    collaborator_name="CustomerSupportAgent",
                    collaboration_instruction="Route Customer support(FAQ) questions to this agent",
                    relay_conversation_history=True

                ),
                AgentCollaborator(
                    agent_alias=content_generation_agent_alias,
                    collaborator_name="WorkshopContentGenerationAgent",
                    collaboration_instruction="Route all workshop content generation questions to this agent",
                    relay_conversation_history=True

                ),
            ]

        )
        self.supervisor_agent_alias = AgentAlias(
            self,
            "SupervisorAgentAlias",
            agent=self.supervisor_agent,
            description="Supervises and orchestrates all the other agents"
        )







        # Create A FAQ Agent


