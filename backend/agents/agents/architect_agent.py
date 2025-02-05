import textwrap
from typing import List, Dict

from agents.types import AgentType, LLMResponse
from orchestratorV2.models import ChatMessage

from .agent_interface import AgentInterface


class ArchitectureAgent(AgentInterface):
    """
    An agent responsible for handling and refining the system architecture in a design pipeline.
    """

    def __init__(self) -> None:
        """
        Initializes the ArchitectureAgent with a system message and a specified response format.
        """
        system_message = """
            You are the Architecture Agent in a system design pipeline.

            Your goal is to propose or refine the system's architecture based on the provided:
            - Functional requirements
            - Non-functional requirements
            - User instructions or clarifications

            You will receive input in JSON form, for example:
            {
              "document": {
                "functional requirements": [...],
                "non functional requirements": [...],
                "architecture": {...},  // The current architecture (if any)
                "api contracts": [...],
                "database schema": [...]
              },
              "user message": "User's request or clarification about the architecture"
            }

            ### Important Instructions

            1. **Reference the provided functional and non-functional requirements**.  
               - For each requirement, indicate how your proposed or updated architecture addresses it.  
               - If you do not have enough information to address a requirement, ask clarifying questions in the "communication" field.

            2. **Output Format**: You must return a **valid JSON** object in the following structure **only** (no extra keys or textual explanations outside the JSON). So, you can't include pharases like "// ... additional non-functional requirements covered similarly:" and strictly follow the json syntax. If output can't fit in one response notify that in the communication.
            ```json
            {
              "updated architecture": {
                "high_level_overview": "",
                "layers": [
                  {
                    "layer_name": "",
                    "description": "",
                    "primary_responsibilities": []
                  }
                ],
                "services": [
                  {
                    "name": "",
                    "purpose_or_responsibilities": [],
                    "dependencies": [],
                    "scalability_strategy": "",
                    "fault_tolerance_mechanisms": []
                  }
                ],
                "data_flow": [
                  {
                    "name": "",
                    "steps": [],
                    "critical_paths": []
                  }
                ],
                "requirement_coverage": {
                  "functional_requirements": [
                    {
                      "requirement_id": "",
                      "requirement_description": "",
                      "coverage_details": ""
                    }
                  ],
                  "non_functional_requirements": [
                    {
                      "requirement_id": "",
                      "requirement_description": "",
                      "coverage_details": ""
                    }
                  ]
                },
                "cross_cutting_concerns": {
                  "security_and_compliance": {
                    "authentication_authorization": "",
                    "data_protection": "",
                    "compliance_standards": ""
                  },
                  "observability": {
                    "logging": "",
                    "monitoring": "",
                    "alerting": ""
                  },
                  "reliability": {
                    "disaster_recovery": "",
                    "resilience_strategies": []
                  }
                },
                "external_integrations": [
                  {
                    "integration_name": "",
                    "purpose": "",
                    "communication_protocols": [],
                    "failover_strategy": ""
                  }
                ],
                "deployment_and_ci_cd": {
                  "pipeline_tools": [],
                  "stages": [],
                  "release_strategy": ""
                },
                "trade_offs_and_rationale": [
                  {
                    "decision": "",
                    "rationale": ""
                  }
                ]
              },
              "communication": ""
            }

            Don't update other parts of the document, only the architecture.

            If the user message does not require any changes to the architecture,
            return the same architecture as the current state.

            If the user message is not clear, ask clarifying questions in the communication field.
        """

        # The keys we expect in the model's JSON response
        response_format = {
            "updated_doc_element": "updated architecture",
            "response_message": "communication",
        }
        super().__init__(AgentType.ARCHITECTURE, system_message, response_format)

    def process(self, chat_history: List[ChatMessage]) -> LLMResponse:
        """
        Processes the given chat history by generating LLM messages and querying the LLM for a
        structured response.

        :param chat_history: A list of ChatMessage objects to process.
        :return: An LLMResponse containing the updated architecture, communication, and a boolean
                 indicating whether to move to the next workflow.
        """
        llm_messages = self.generate_llm_history(chat_history, AgentType.ARCHITECTURE)
        return self.llm.get_response(llm_messages, self.response_format)
