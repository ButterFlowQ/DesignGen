from typing import Optional

from .agent_interface import AgentInterface
from .requirement_agent import RequirementAgent
from .types import AgentType


class AgentFactory:
    @staticmethod
    def create_agent(agent_type: AgentType) -> Optional[AgentInterface]:
        """
        Creates and returns an agent based on the specified AgentType.
        
        Args:
            agent_type: The type of agent to create
            
        Returns:
            An instance of the specified agent, or None if the agent type is not supported
        """
        if agent_type == AgentType.REQUIREMENT:
            return RequirementAgent()
        
        # Add other agent types here as they are implemented
        return None 