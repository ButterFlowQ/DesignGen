from .agent_interface import AgentInterface
from .requirement_agent import RequirementAgent
from .types import AgentType


class AgentFactory:
    @staticmethod
    def create_agent(agent_type: AgentType) -> AgentInterface:
        if agent_type == AgentType.REQUIREMENT:
            return RequirementAgent()

        # Add other agent types here as they are implemented
        raise NotImplementedError(f"Agent type {agent_type} is not implemented")
    