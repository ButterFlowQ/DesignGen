from typing import List

from agents.types import AgentType, LLMResponse, LLMMessage

from .agent_interface import AgentInterface


class HtmlGeneratorAgent(AgentInterface):
    """
    An agent responsible for converting a JSON document into an HTML representation.
    """

    def __init__(self) -> None:
        """
        Initializes the HTML generator agent with a system message and a specified response format.
        """
        system_message = """
            You are an HTML generator agent. Your role is to convert a serialized JSON document into an HTML representation.
            You will receive a user message containing a stringified JSON document. Your task is to parse the JSON and generate an HTML representation of the document.
            The output should be a JSON object with a single key "html" containing the generated HTML as a string.
            Example input:
            {
                "functional requirements": [
                    "Current functional requirement 1",
                    "Current functional requirement 2"
                ],
                "non functional requirements": [
                    "Current non-functional requirement 1",
                    "Current non-functional requirement 2",
                ],
                "architecture": {},
                "api contract": {},
                "database schema": {},
            }
            Example output:
            {
                "html": "</head><body><p>...</p><p>...</p>"
            }
        """

        # The keys we expect in the model's JSON response
        response_format = {
            "response_message": "html",
        }
        super().__init__(
            AgentType.HTML_GENERATOR,
            system_message,
            response_format,
            # "openai:gpt-4o-2024-08-06",
        )

    def getHtml(self, doc):
        llm_message = LLMMessage(role="user", content=doc)
        return self.llm.get_response([llm_message], self.response_format)
