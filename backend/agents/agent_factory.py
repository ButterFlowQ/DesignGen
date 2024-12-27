from .agents.agent_interface import AgentInterface
from .agents.requirement_agent import RequirementAgent
from .types import AgentType


class AgentFactory:
    """
    A factory for creating instances of agents based on the specified AgentType.
    """

    _agent_registry = {
        AgentType.REQUIREMENT: RequirementAgent,
    }

    @staticmethod
    def create_agent(agent_type: AgentType) -> AgentInterface:
        """
        Creates and returns an agent instance for the specified AgentType.

        :param agent_type: The type of the agent to create.
        :return: An instance of a class implementing AgentInterface.
        :raises NotImplementedError: If the requested agent type is not yet supported.
        """
        agent_class = AgentFactory._agent_registry.get(agent_type)
        if agent_class is None:
            raise NotImplementedError(
                f"Agent type '{agent_type}' is not implemented or is unregistered."
            )
        return agent_class()
