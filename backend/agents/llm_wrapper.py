import json
from typing import List, Dict

import aisuite as ai
from .types import LLMResponse


class LLMWrapper:
    """
    A wrapper around an AI client for processing messages and retrieving structured responses.
    """

    def __init__(self) -> None:
        """
        Initializes the LLMWrapper with the default AI client and model.
        """
        self.client = ai.Client()
        self.model = "openai:o1-2024-12-17" # "anthropic:claude-3-5-sonnet-20241022" # o1-mini-2024-09-12, o1-2024-12-17, gpt-4o-2024-08-06

    def get_response(
        self, messages: List[Dict[str, str]], expected_fields: Dict[str, str]
    ) -> LLMResponse:
        """
        Gets a response from the LLM.
        """

        try:
            raw_response = self._get_completion(messages)

            parsed_response = json.loads(raw_response)
            if not all(key in parsed_response for key in expected_fields.values()):
                raise ValueError("Missing required fields in the model response.")

            resp = LLMResponse()
            resp["raw_response"] = raw_response

            for key, value in expected_fields.items():
                resp[key] = parsed_response[value]

            return resp
        except Exception as exc:
            # For unexpected exceptions, raise them directly
            raise exc

    def _get_completion(self, messages: List[Dict[str, str]]) -> str:
        """
        Sends a chat completion request to the AI client.

        :param messages: A list of dicts containing the conversation history with 'role' and
            'content' keys.
        :return: The AI model's response content as a string.
        """
        response = self.client.chat.completions.create(
            model=self.model, messages=messages, temperature=0.25, response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
