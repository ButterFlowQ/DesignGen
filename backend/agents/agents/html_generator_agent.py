from agents.types import AgentType, LLMResponse

from .simple_agent_interface import SimpleAgentInterface


class HtmlGeneratorAgent(SimpleAgentInterface):
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

            Keep the title tag of the document as Software Design Document.
            Use table tags to display data where appropriate.
        """

        # The keys we expect in the model's JSON response
        response_format = {
            "response_message": "html",
        }
        super().__init__(
            AgentType.HTML_GENERATOR,
            system_message,
            response_format,
            "openai:gpt-4o-2024-08-06",
        )

    def process(self, message: str) -> LLMResponse:
        llm_messages = self.generate_llm_history(message)
        return self.llm.get_response(llm_messages, self.response_format)