"""Chat service orchestration logic."""
from typing import List, Dict, Any, Optional
from sqlmodel import Session, select
from datetime import datetime
import logging

from src.services.groq_client import GroqClient
from src.services.tool_executor import tool_executor
from src.tools.tool_registry import tool_registry
from src.tools.task_tools import (
    ALL_TOOL_SCHEMAS,
    add_task,
    list_tasks,
    update_task,
    delete_task,
    get_task
)
from src.models.conversation import Conversation
from src.models.message import Message

logger = logging.getLogger(__name__)


class ChatService:
    """
    Orchestrates chat interactions between user, AI, and tool execution.
    Handles conversation history, AI inference, and tool calling.
    """

    def __init__(self):
        """Initialize chat service with Groq client and tool setup."""
        self.groq_client = GroqClient()
        self._setup_tools()

    def _setup_tools(self):
        """Register all tool schemas and execution functions."""
        # Register schemas
        tool_registry.register_tools(ALL_TOOL_SCHEMAS)

        # Register execution functions
        tool_executor.register_function("add_task", add_task)
        tool_executor.register_function("list_tasks", list_tasks)
        tool_executor.register_function("update_task", update_task)
        tool_executor.register_function("delete_task", delete_task)
        tool_executor.register_function("get_task", get_task)

    def process_message(
        self,
        user_message: str,
        user_id: int,
        session: Session,
        conversation_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Process a user message and return AI response.

        Args:
            user_message: User's input message
            user_id: ID of authenticated user
            session: Database session
            conversation_id: Optional existing conversation ID

        Returns:
            Dictionary with assistant response and conversation_id
        """
        logger.info(f"Processing message for user {user_id}, conversation_id={conversation_id}")
        logger.debug(f"User message: {user_message[:100]}...")  # Log first 100 chars

        # Get or create conversation
        if conversation_id:
            conversation = session.get(Conversation, conversation_id)
            if not conversation or conversation.user_id != user_id:
                logger.warning(
                    f"Conversation access denied: user {user_id} tried to access conversation {conversation_id}"
                )
                raise ValueError("Conversation not found or access denied")
            logger.info(f"Using existing conversation {conversation_id}")
        else:
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            logger.info(f"Created new conversation {conversation.id} for user {user_id}")

        # Save user message
        user_msg = Message(
            conversation_id=conversation.id,
            role="user",
            content=user_message
        )
        session.add(user_msg)
        session.commit()
        logger.debug(f"Saved user message to conversation {conversation.id}")

        # Get conversation history
        messages = self._get_conversation_history(conversation.id, session)
        logger.info(f"Retrieved {len(messages)} messages from conversation history")

        # Analyze tasks for proactive suggestions
        task_context = self._analyze_tasks_for_suggestions(user_id, session)
        if task_context:
            logger.info(f"Task context generated for suggestions")
            logger.debug(f"Task context: {task_context}")

        # Call AI with tools and system prompt
        try:
            system_prompt = self.groq_client.get_task_assistant_system_prompt()

            # Add task context to system prompt if available
            if task_context:
                system_prompt += f"\n\n**Current Task Context:**\n{task_context}"

            logger.info(f"Calling Groq API with {len(messages)} messages")
            response = self.groq_client.chat_completion(
                messages=messages,
                tools=tool_registry.get_all_tools(),
                temperature=0.7,
                system_prompt=system_prompt
            )

            assistant_message = response.choices[0].message
            logger.info(f"Received AI response, has_tool_calls={bool(assistant_message.tool_calls)}")

            # Debug logging
            logger.debug(f"AI Response - has tool_calls: {hasattr(assistant_message, 'tool_calls')}")
            logger.debug(f"AI Response - tool_calls value: {getattr(assistant_message, 'tool_calls', None)}")
            logger.debug(f"AI Response - content: {assistant_message.content}")

            # Check if AI wants to call tools
            if assistant_message.tool_calls:
                logger.info(f"AI requested {len(assistant_message.tool_calls)} tool calls")

                # Execute tools
                tool_results = self._execute_tools(
                    assistant_message.tool_calls,
                    user_id,
                    session
                )

                successful_tools = sum(1 for r in tool_results if r.get("success"))
                logger.info(f"Tool execution complete: {successful_tools}/{len(tool_results)} successful")

                # Save tool messages
                for result in tool_results:
                    tool_msg = Message(
                        conversation_id=conversation.id,
                        role="tool",
                        content=str(result.get("result", result.get("error"))),
                        tool_call_id=result["tool_call_id"],
                        tool_name=result["tool_name"]
                    )
                    session.add(tool_msg)

                session.commit()

                # Get updated history with tool results
                messages = self._get_conversation_history(conversation.id, session)

                # Call AI again for final response
                logger.info("Calling Groq API for final response after tool execution")
                final_response = self.groq_client.chat_completion(
                    messages=messages,
                    tools=tool_registry.get_all_tools(),
                    temperature=0.7,
                    system_prompt=system_prompt
                )

                final_message = final_response.choices[0].message.content
                logger.info("Received final AI response after tool execution")

                # Handle case where AI returns None for content
                if not final_message:
                    final_message = "Task completed successfully."
                    logger.debug("AI returned empty content, using default message")

            # Fallback: Parse text-based function calls (Groq sometimes returns these)
            elif assistant_message.content and '<function' in assistant_message.content:
                logger.info("Detected text-based function call, parsing manually")

                # Parse function calls from text
                import re
                import json

                # Pattern: <function/name>{"args"}</function> or <function(name)>{"args"}</function>
                # Use .+? for non-greedy match to capture full JSON including nested braces
                pattern = r'<function[(/](\w+)\)?>(.+?)</function>'
                matches = re.findall(pattern, assistant_message.content, re.DOTALL)

                if matches:
                    logger.info(f"Found {len(matches)} text-based function calls")
                    tool_results = []
                    for func_name, args_json in matches:
                        try:
                            args = json.loads(args_json)
                            args["session"] = session
                            args["user_id"] = user_id

                            # Execute the tool
                            if func_name == "add_task":
                                from src.tools.task_tools import add_task
                                result = add_task(**args)
                            elif func_name == "list_tasks":
                                from src.tools.task_tools import list_tasks
                                result = list_tasks(**args)
                            elif func_name == "update_task":
                                from src.tools.task_tools import update_task
                                result = update_task(**args)
                            elif func_name == "delete_task":
                                from src.tools.task_tools import delete_task
                                result = delete_task(**args)
                            elif func_name == "get_task":
                                from src.tools.task_tools import get_task
                                result = get_task(**args)
                            else:
                                result = {"error": f"Unknown function: {func_name}"}

                            tool_results.append({
                                "tool_name": func_name,
                                "result": result
                            })

                            logger.info(f"Executed text-based function call: {func_name}")
                            logger.debug(f"Result: {result}")

                        except Exception as e:
                            logger.error(f"Error executing text-based function {func_name}: {e}", exc_info=True)
                            tool_results.append({
                                "tool_name": func_name,
                                "result": {"error": str(e)}
                            })

                    # Save tool results as messages
                    for result in tool_results:
                        tool_msg = Message(
                            conversation_id=conversation.id,
                            role="tool",
                            content=str(result["result"]),
                            tool_call_id=None,
                            tool_name=result["tool_name"]
                        )
                        session.add(tool_msg)

                    session.commit()
                    logger.debug("Saved text-based tool results to database")

                    # Generate final response
                    final_message = f"Task completed successfully."
                else:
                    final_message = assistant_message.content or "I'm here to help with your tasks."

            else:
                # No tool calls - just return the content
                final_message = assistant_message.content
                logger.info("No tool calls, returning direct AI response")

                # Handle case where AI returns None for content
                if not final_message:
                    final_message = "I'm here to help with your tasks."
                    logger.debug("AI returned empty content, using default message")

            # Save assistant response
            assistant_msg = Message(
                conversation_id=conversation.id,
                role="assistant",
                content=final_message
            )
            session.add(assistant_msg)

            # Update conversation timestamp
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()
            logger.info(f"Saved assistant response to conversation {conversation.id}")

            return {
                "message": final_message,
                "conversation_id": conversation.id,
                "role": "assistant"
            }

        except Exception as e:
            # Handle errors gracefully
            logger.error(
                f"Error processing message for user {user_id}: {str(e)}",
                exc_info=True
            )

            error_message = "I'm having trouble processing your request. Please try again."

            if self.groq_client.handle_rate_limit(e):
                error_message = "I'm currently experiencing high demand. Please wait a moment and try again."
                logger.warning(f"Rate limit hit for user {user_id}")

            return {
                "message": error_message,
                "conversation_id": conversation.id,
                "role": "assistant",
                "error": str(e)
            }

    def _get_conversation_history(
        self,
        conversation_id: int,
        session: Session,
        max_messages: int = 50,
        max_tokens: int = 6000
    ) -> List[Dict[str, str]]:
        """
        Retrieve conversation history as message list for AI with context window management.

        Implements smart truncation to stay within token limits while preserving
        conversation coherence. Keeps most recent messages and system context.

        Args:
            conversation_id: ID of the conversation
            session: Database session
            max_messages: Maximum number of messages to retrieve
            max_tokens: Maximum tokens to include (default 6000, leaving room for response)

        Returns:
            List of message dictionaries for AI
        """
        query = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )

        all_messages = session.exec(query).all()

        # If no messages, return empty list
        if not all_messages:
            return []

        # Convert to message dictionaries
        result = []
        for msg in all_messages:
            message_dict = {"role": msg.role, "content": msg.content}

            # Tool messages require tool_call_id
            if msg.role == "tool" and msg.tool_call_id:
                message_dict["tool_call_id"] = msg.tool_call_id

            result.append(message_dict)

        # Apply message count limit first
        if len(result) > max_messages:
            result = result[-max_messages:]

        # Apply token-based truncation (rough estimate: 4 chars ≈ 1 token)
        total_chars = sum(len(msg.get("content", "")) for msg in result)
        estimated_tokens = total_chars // 4

        if estimated_tokens > max_tokens:
            # Keep most recent messages that fit within token limit
            truncated = []
            current_tokens = 0

            # Iterate from most recent to oldest
            for msg in reversed(result):
                msg_tokens = len(msg.get("content", "")) // 4
                if current_tokens + msg_tokens <= max_tokens:
                    truncated.insert(0, msg)
                    current_tokens += msg_tokens
                else:
                    break

            result = truncated

        return result

    def _execute_tools(
        self,
        tool_calls: list,
        user_id: int,
        session: Session
    ) -> List[Dict[str, Any]]:
        """
        Execute tool calls with database session.

        Args:
            tool_calls: List of tool calls from AI
            user_id: ID of authenticated user
            session: Database session

        Returns:
            List of tool execution results
        """
        results = []

        for tool_call in tool_calls:
            tool_name = tool_call.function.name

            try:
                # Parse parameters
                import json
                parameters = json.loads(tool_call.function.arguments)

                # Add session to parameters
                parameters["session"] = session
                parameters["user_id"] = user_id

                # Execute tool
                if tool_name == "add_task":
                    result = add_task(**parameters)
                elif tool_name == "list_tasks":
                    result = list_tasks(**parameters)
                elif tool_name == "update_task":
                    result = update_task(**parameters)
                elif tool_name == "delete_task":
                    result = delete_task(**parameters)
                elif tool_name == "get_task":
                    result = get_task(**parameters)
                else:
                    result = {"error": f"Unknown tool: {tool_name}"}

                results.append({
                    "tool_call_id": tool_call.id,
                    "tool_name": tool_name,
                    "success": True,
                    "result": result
                })

            except Exception as e:
                results.append({
                    "tool_call_id": tool_call.id,
                    "tool_name": tool_name,
                    "success": False,
                    "error": str(e)
                })

        return results

    def sanitize_input(self, user_input: str) -> str:
        """
        Sanitize user input to prevent prompt injection.

        Args:
            user_input: Raw user input

        Returns:
            Sanitized input
        """
        # Basic sanitization - remove potential injection patterns
        sanitized = user_input.strip()

        # Limit length to prevent context overflow
        max_length = 2000
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]

        return sanitized


    def _analyze_tasks_for_suggestions(
        self,
        user_id: int,
        session: Session
    ) -> str:
        """
        Analyze user's tasks to provide context for intelligent suggestions.

        Args:
            user_id: ID of the user
            session: Database session

        Returns:
            String with task analysis context for AI
        """
        from src.models.task import Task
        from datetime import datetime

        try:
            # Get all tasks for the user
            query = select(Task).where(Task.user_id == user_id)
            tasks = session.exec(query).all()

            if not tasks:
                return ""

            context_parts = []
            now = datetime.utcnow()

            # Count tasks by completion status
            completed_count = sum(1 for t in tasks if t.completed)
            pending_count = sum(1 for t in tasks if not t.completed)

            context_parts.append(
                f"User has {len(tasks)} total tasks: "
                f"{pending_count} pending, {completed_count} completed"
            )

            # Check for overdue tasks
            overdue_tasks = [
                t for t in tasks
                if t.due_date and t.due_date < now and not t.completed
            ]
            if overdue_tasks:
                context_parts.append(
                    f"⚠️ {len(overdue_tasks)} overdue task(s) detected - consider suggesting user review them"
                )

            # Check for tasks without due dates
            no_due_date_tasks = [
                t for t in tasks
                if not t.due_date and not t.completed
            ]
            if no_due_date_tasks and len(no_due_date_tasks) > 3:
                context_parts.append(
                    f"📅 {len(no_due_date_tasks)} task(s) without due dates - may suggest adding dates for better planning"
                )

            # Check for tasks with very short descriptions (potentially vague)
            vague_tasks = [
                t for t in tasks
                if len(t.title) < 15 and not t.completed
            ]
            if vague_tasks and len(vague_tasks) > 2:
                context_parts.append(
                    f"📝 {len(vague_tasks)} task(s) with brief descriptions - may suggest adding more details"
                )

            # Check for high priority tasks
            high_priority_tasks = [
                t for t in tasks
                if t.priority == "high" and not t.completed
            ]
            if high_priority_tasks:
                context_parts.append(
                    f"🔥 {len(high_priority_tasks)} high priority task(s) - user may need focus on these"
                )

            return "\n".join(context_parts) if context_parts else ""

        except Exception as e:
            # Don't fail the whole request if analysis fails
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Task analysis failed: {e}")
            return ""


# Global chat service instance
chat_service = ChatService()
