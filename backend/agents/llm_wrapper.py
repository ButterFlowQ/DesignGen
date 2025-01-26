import json
from typing import List, Dict
import logging
import re

import aisuite as ai
from .types import LLMResponse

# Create a logger for this module.
logger = logging.getLogger(__name__)


class LLMWrapper:
    """
    A wrapper around an AI client for processing messages and retrieving structured responses.
    """

    def __init__(self, model: str = "openai:o1-mini-2024-09-12") -> None:
        """
        Initializes the LLMWrapper with the default AI client and model.
        """
        self.client = ai.Client()
        self.model = model  # "anthropic:claude-3-5-sonnet-20241022" # o1-mini-2024-09-12, o1-2024-12-17, gpt-4o-2024-08-06, o1-preview-2024-09-12

    def get_response(
        self, messages: List[Dict[str, str]], expected_fields: Dict[str, str]
    ) -> LLMResponse:
        """
        Gets a response from the LLM.
        """

        try:
            raw_response = self._get_completion(messages)
            logger.info(raw_response)
            # print to be removed after logging works properly
            print(repr(raw_response))

            parsed_response = self.parse_response(raw_response)
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
        if self.model.startswith("openai:o1"):
            # current o1-preview-2024-09-12 model doesn't support response_format as json_object, o1 models support json_object start from 2024-12-17
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
        else:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.25,
                response_format={"type": "json_object"},
            )
        return response.choices[0].message.content

    def parse_response(self, raw_response: str) -> Dict[str, str]:
        # Some models return extra text before and after the JSON object, so we need to extract just the JSON portion
        start_idx = raw_response.find("{")
        end_idx = raw_response.rfind("}")
        if start_idx == -1 or end_idx == -1:
            raise ValueError("No valid JSON object found in model response")
        json_str = raw_response[start_idx : end_idx + 1]
        pattern = r"\"(.*?)\""

        # Function to escape newlines within string literals
        def escape_newlines(match):
            # Replace actual newlines with escaped newlines
            escaped_str = match.group(1).replace("\n", "\\n").replace("\r", "\\r")
            return f'"{escaped_str}"'

        # Apply the regex to escape newlines within strings
        fixed_json_str = re.sub(pattern, escape_newlines, json_str, flags=re.DOTALL)

        try:
            parsed_response = json.loads(fixed_json_str)
            return parsed_response
        except json.JSONDecodeError as e:
            logger.error("JSONDecodeError: %s", e)
            logger.error("Original JSON string: %s", json_str)
            logger.error("Fixed JSON string: %s", fixed_json_str)
            raise e
