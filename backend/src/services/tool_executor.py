"""Tool executor service for executing AI-requested tool calls."""
from typing import Dict, Any, Callable, Optional
import json
import logging

logger = logging.getLogger(__name__)


class ToolExecutor:
    """
    Executes tool calls requested by the AI.
    Maps tool names to Python functions and handles execution.
    """

    def __init__(self):
        """Initialize tool executor with empty function registry."""
        self._functions: Dict[str, Callable] = {}

    def register_function(self, tool_name: str, function: Callable) -> None:
        """
        Register a Python function for a tool.

        Args:
            tool_name: Name of the tool (must match schema name)
            function: Python function to execute for this tool
        """
        self._functions[tool_name] = function
        logger.info(f"Registered tool function: {tool_name}")

    def execute_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        user_id: int
    ) -> Dict[str, Any]:
        """
        Execute a tool call with given parameters.

        Args:
            tool_name: Name of the tool to execute
            parameters: Parameters for the tool (from AI)
            user_id: ID of the authenticated user (for data scoping)

        Returns:
            Dictionary with execution result

        Raises:
            KeyError: If tool not registered
            Exception: If tool execution fails
        """
        if tool_name not in self._functions:
            error_msg = f"Tool '{tool_name}' not registered"
            logger.error(f"Tool execution failed: {error_msg}")
            raise KeyError(error_msg)

        try:
            # Add user_id to parameters for data scoping
            parameters["user_id"] = user_id

            logger.info(f"Executing tool: {tool_name} for user {user_id}")
            logger.debug(f"Tool parameters: {parameters}")

            # Execute the function
            result = self._functions[tool_name](**parameters)

            logger.info(f"Tool execution successful: {tool_name}")
            logger.debug(f"Tool result: {result}")

            return {
                "success": True,
                "result": result
            }

        except Exception as e:
            logger.error(
                f"Tool execution failed: {tool_name} for user {user_id}",
                exc_info=True
            )
            logger.error(f"Error details: {str(e)}")

            return {
                "success": False,
                "error": str(e)
            }

    def execute_tool_calls(
        self,
        tool_calls: list,
        user_id: int
    ) -> list:
        """
        Execute multiple tool calls from AI response.

        Args:
            tool_calls: List of tool call objects from OpenAI response
            user_id: ID of the authenticated user

        Returns:
            List of tool execution results
        """
        results = []
        logger.info(f"Executing {len(tool_calls)} tool calls for user {user_id}")

        for tool_call in tool_calls:
            tool_name = tool_call.function.name

            # Parse parameters from JSON string
            try:
                parameters = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError as e:
                error_msg = "Invalid JSON parameters"
                logger.error(
                    f"JSON decode error for tool {tool_name}: {str(e)}",
                    exc_info=True
                )
                results.append({
                    "tool_call_id": tool_call.id,
                    "success": False,
                    "error": error_msg
                })
                continue

            # Execute tool
            result = self.execute_tool(tool_name, parameters, user_id)
            result["tool_call_id"] = tool_call.id
            result["tool_name"] = tool_name

            results.append(result)

        successful = sum(1 for r in results if r.get("success"))
        logger.info(
            f"Tool execution batch complete: {successful}/{len(results)} successful"
        )

        return results

    def has_function(self, tool_name: str) -> bool:
        """
        Check if a function is registered for a tool.

        Args:
            tool_name: Name of the tool

        Returns:
            True if function registered, False otherwise
        """
        return tool_name in self._functions


# Global tool executor instance
tool_executor = ToolExecutor()
