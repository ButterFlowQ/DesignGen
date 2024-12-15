import aisuite as ai

class LLMWrapper:
    def __init__(self):
        self.client = ai.Client()
        self.model = "anthropic:claude-3-5-sonnet-20241022"

    def get_completion(self, messages):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.25
        )
        return response.choices[0].message.content
