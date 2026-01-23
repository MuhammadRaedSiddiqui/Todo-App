"""Tool registry for MCP tool schemas."""
from typing import List, Dict, Any


class ToolRegistry:
    """
    Registry for managing MCP (Model Context Protocol) tool schemas.
    Provides centralized access to tool definitions for AI function calling.
    """

    def __init__(self):
        """Initialize empty tool registry."""
        self._tools: Dict[str, Dict[str, Any]] = {}

    def register_tool(self, tool_schema: Dict[str, Any]) -> None:
        """
        Register a tool schema.

        Args:
            tool_schema: Tool definition following OpenAI function calling format
                        Must include 'type' and 'function' with 'name' field
        """
        if "function" not in tool_schema or "name" not in tool_schema["function"]:
            raise ValueError("Tool schema must include function.name")

        tool_name = tool_schema["function"]["name"]
        self._tools[tool_name] = tool_schema

    def register_tools(self, tool_schemas: List[Dict[str, Any]]) -> None:
        """
        Register multiple tool schemas.

        Args:
            tool_schemas: List of tool definitions
        """
        for schema in tool_schemas:
            self.register_tool(schema)

    def get_tool(self, tool_name: str) -> Dict[str, Any]:
        """
        Get a specific tool schema by name.

        Args:
            tool_name: Name of the tool

        Returns:
            Tool schema dictionary

        Raises:
            KeyError: If tool not found
        """
        if tool_name not in self._tools:
            raise KeyError(f"Tool '{tool_name}' not found in registry")
        return self._tools[tool_name]

    def get_all_tools(self) -> List[Dict[str, Any]]:
        """
        Get all registered tool schemas.

        Returns:
            List of all tool schemas
        """
        return list(self._tools.values())

    def get_tool_names(self) -> List[str]:
        """
        Get names of all registered tools.

        Returns:
            List of tool names
        """
        return list(self._tools.keys())

    def has_tool(self, tool_name: str) -> bool:
        """
        Check if a tool is registered.

        Args:
            tool_name: Name of the tool

        Returns:
            True if tool exists, False otherwise
        """
        return tool_name in self._tools

    def clear(self) -> None:
        """Clear all registered tools."""
        self._tools.clear()


# Global tool registry instance
tool_registry = ToolRegistry()
