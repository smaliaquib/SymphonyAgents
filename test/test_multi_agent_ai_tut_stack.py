import aws_cdk as core
import aws_cdk.assertions as assertions

from multi_agent_ai_tut.multi_agent_ai_tut_stack import MultiAgentAiTutStack

# example tests. To run these tests, uncomment this file along with the example
# resource in multi_agent_ai_tut/multi_agent_ai_tut_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MultiAgentAiTutStack(app, "multi-agent-ai-tut")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
