"""Agent module."""

from pydantic_ai import Agent
from pydantic_ai import Tool
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models import ModelSettings
from extendable_agent.hub import ToolsHub
from extendable_agent.tools import load_code_as_module


class AgentModel:
    """Agent model."""

    def __init__(
        self,
        model: str = "openai:gpt-4o",
        name: str = "Agent",
        system_prompt: str = "You are a helpful assistant.",
        function_tools: list[str] | None = None,
        model_settings: dict | None = None,
        result_type: dict | None = None,
        mcp_servers: list[tuple[str, list[str]]] | None = None,
    ):
        """Initialize the agent model.

        Args:
            model (str): The model name.
            name (str): The name of the agent.
            system_prompt (str): The system prompt for the agent.
            function_tools (list[str]): The function tool names for the agent.
            model_settings (dict): The model settings for the agent.
            result_type (dict): The result type for the agent.
            mcp_servers (list[tuple[str, list[str]]]): The MCP servers for the agent.
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt
        self.function_tools = function_tools
        self.model_settings = model_settings
        self.result_type = result_type
        self.mcp_servers = mcp_servers

    def get_pydantic_agent(self, model: str, hf_tools: list[Tool]) -> Agent:
        """Get the agent config from DB and convert to Pydantic agent."""
        tools = []
        if self.function_tools:
            tools_hub = ToolsHub()
            for tool_name in self.function_tools:
                function_code = tools_hub.get_file_from_github(tool_name)
                if not function_code:
                    continue
                module = load_code_as_module(function_code)
                tools.append(getattr(module, tool_name))

        model_settings = self.model_settings or {}

        if self.mcp_servers:
            servers = [
                MCPServerStdio(command, args) for command, args in self.mcp_servers
            ]
            return Agent(
                model=model or self.model,  # type: ignore[arg-type]
                name=self.name,
                system_prompt=self.system_prompt,
                model_settings=ModelSettings(**model_settings),
                tools=tools + hf_tools,
                mcp_servers=servers,
            )
        return Agent(
            model=model or self.model,  # type: ignore[arg-type]
            name=self.name,
            system_prompt=self.system_prompt,
            model_settings=ModelSettings(**model_settings),
            tools=tools + hf_tools,
        )
