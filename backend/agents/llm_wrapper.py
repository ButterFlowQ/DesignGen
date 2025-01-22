import json
import traceback
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
        Attempts to retrieve a valid structured response from the AI model.

        :param messages: A list of message dictionaries with 'role' and 'content' fields.
        :param expected_fields: A list of strings specifying the required JSON keys in the
            model's response. The list order corresponds to how they're assigned in LLMResponse.
        :return: An LLMResponse object containing the updated workflow doc, a response message,
            and a boolean indicating if the workflow should move to the next step.
        :raises ValueError: If a valid response is not obtained within the retry limit or if any
            required fields are missing from the model response.
        """
        max_retries = 3
        attempt_count = 0
        last_exception = None
        error_trace = ""

        while attempt_count < max_retries:
            try:
                if attempt_count == 0:
                    raw_response = self._get_completion(messages)
                else:
                    # Append an error message hinting at the missing format
                    error_message = {
                        "role": "user",
                        "content": (
                            "The previous response was not in the correct format. Please provide "
                            "the response in the exact JSON format specified in the system "
                            f"message. Error: {last_exception}"
                        ),
                    }
                    messages.append(error_message)
                    raw_response = self._get_completion(messages)

                parsed_response = json.loads(raw_response)
                if not all(key in parsed_response for key in expected_fields.values()):
                    raise ValueError("Missing required fields in the model response.")

                resp = LLMResponse()
                for key, value in expected_fields.items():
                    resp[key] = parsed_response[value]
                return resp
            except (ValueError, AttributeError, TypeError, json.JSONDecodeError) as exc:
                attempt_count += 1
                last_exception = exc
                error_trace = traceback.format_exc()
            except Exception as exc:
                # For unexpected exceptions, raise them directly
                raise exc

        raise ValueError(
            f"Failed to get a valid response after {max_retries} attempts.\n"
            f"Last error: {last_exception}\nStack trace:\n{error_trace}"
        )

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
