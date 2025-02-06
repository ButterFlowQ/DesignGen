from plantweb.render import render
from agents.types import AgentType, LLMResponse

from .simple_agent_interface import SimpleAgentInterface


class JavaLLDHTMLGeneratorAgent(SimpleAgentInterface):
    """
    An agent responsible for converting a JSON document into an HTML representation.
    """

    def __init__(self) -> None:
        """
        Initializes the HTML generator agent with a system message and a specified response format.
        """
        system_message = """
            You are an plantuml generator agent. Convert to following JSON into an plantuml representation.
            Example input:
            {
                .... 
            }
            Example output:
            {
                plantuml : stringified plantuml
            }

            Output should be a Json object with a single key "plantuml" containing the generated plantuml.
            Start the plantuml with @startuml.
            End the plantuml with @enduml.
            Do not include any other text in the plantuml.
        """

        # The keys we expect in the model's JSON response
        response_format = {
            "plantuml": "plantuml",
        }
        super().__init__(
            AgentType.HTML_GENERATOR,
            system_message,
            response_format,
        )

    def process(self, message: str) -> LLMResponse:
        llm_messages = self.generate_llm_history(message)
        plantuml = self.llm.get_response(llm_messages, self.response_format)["plantuml"]
        return {"response_message": plantuml}
