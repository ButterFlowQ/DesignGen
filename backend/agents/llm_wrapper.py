import aisuite as ai
from .types import LLMResponse
import json

class LLMWrapper:
    def __init__(self):
        self.client = ai.Client()
        self.model = "anthropic:claude-3-5-sonnet-20241022"

    def get_response(self, messages, response_format):
        max_retries = 3
        current_try = 0
        last_error = None
        
        while current_try < max_retries:
            try:
                if current_try == 0:
                    response = self.get_completion(messages)
                else:
                    # Add error message and retry
                    error_message = {
                        "role": "user", 
                        "content": f"The previous response was not in the correct format. Please provide response in the exact JSON format specified in the system message. Error: {str(last_error)}"
                    }
                    messages.append(error_message)
                    response = self.get_completion(messages)

                parsed_response = json.loads(response)
                
                # Validate required fields
                if not all(key in parsed_response for key in response_format):
                    raise ValueError("Missing required fields in response")
                
                return LLMResponse(
                    move_to_next_workflow=parsed_response["ready_for_next_workflow"],
                    response_message=parsed_response["communication"],
                    updated_workflow_doc=parsed_response["current_workflow_doc"]
                )
                
            except (ValueError, AttributeError, TypeError, json.JSONDecodeError) as e:
                current_try += 1
                last_error = e
        
        raise Exception(f"Failed to get valid response after {max_retries} attempts. Last error: {str(last_error)}")
        
    
    def get_completion(self, messages):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.25
        )
        return response.choices[0].message.content
