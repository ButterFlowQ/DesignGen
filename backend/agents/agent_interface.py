from typing import Dict, List, Tuple, Any

class AgentInterface():
    def __init__(
            self,
            system_message: str,
    ) -> None:
        self.chat_history = []
        self.system_message = {
            "role": "system",
            "content": system_message,
        }
        self.chat_history.append(self.system_message)

    def process(
        self,
        document: Any,
        workflow_element: Any,
        user_message: str,
        context: Any = None,
    ) -> Tuple[Any, str, bool]:
        """
        Process the current workflow element with given inputs.

        Args:
            document: The document being processed
            workflow_element: The current workflow element configuration
            user_message: The user message
            context: Additional contextual information

        Returns:
            Tuple containing:
            - Updated workflow element
            - Response message
            - Boolean indicating whether we are done with the workflow
        """
        pass
