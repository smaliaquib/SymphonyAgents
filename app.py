#!/usr/bin/env python3
import os

import aws_cdk as cdk

from multi_agent_ai_tut.multi_agent_ai_tut_stack import MultiAgentAiTutStack
from multi_agent_ai_tut.rest_api_stack import RestApiStack

app = cdk.App()
multi_agent_ai_tut_stack = MultiAgentAiTutStack(app, "MultiAgentAiTutStack",
                                                )

rest_api_stack = RestApiStack(app, 'RestApiStack',
                              aiAgentId=multi_agent_ai_tut_stack.supervisor_agent.agent_id,
                              aiAgentAlias=multi_agent_ai_tut_stack.supervisor_agent_alias.alias_id)

app.synth()
