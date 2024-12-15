from typing import Dict, List, Tuple, Any

class AgentInterface():

    def process(
        self,
        document: Any,
        workflow_element: Any, 
        chat_history: List[Dict[str, str]],
        context: Any
    ) -> Tuple[Any, str, bool]:
        """
        Process the current workflow element with given inputs.

        Args:
            document: The document being processed
            workflow_element: The current workflow element configuration
            chat_history: List of previous chat messages
            context: Additional contextual information

        Returns:
            Tuple containing:
            - Updated workflow element
            - Response message
            - Boolean indicating whether to proceed to next element
        """
        pass
