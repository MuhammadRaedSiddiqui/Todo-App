"""Groq API client wrapper using OpenAI SDK compatibility."""
import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class GroqClient:
    """
    Wrapper for Groq API using OpenAI SDK compatibility pattern.
    Configures the OpenAI client to use Groq's endpoint.
    Supports both GROQ_* and OPENAI_* environment variable naming.
    """

    def __init__(self):
        """Initialize Groq client with OpenAI SDK."""
        # Support both GROQ_* and OPENAI_* environment variables
        self.base_url = (
            os.getenv("GROQ_BASE_URL") or
            os.getenv("OPENAI_BASE_URL") or
            "https://api.groq.com/openai/v1"
        )
        self.api_key = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.model = (
            os.getenv("GROQ_MODEL") or
            os.getenv("OPENAI_MODEL") or
            "llama-3.3-70b-versatile"
        )

        if not self.api_key:
            raise ValueError(
                "API key required. Set either GROQ_API_KEY or OPENAI_API_KEY environment variable"
            )

        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None
    ) -> Any:
        """
        Create a chat completion using Groq's Llama 3.3 model.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            tools: Optional list of tool definitions for function calling
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            system_prompt: Optional system prompt to prepend to messages

        Returns:
            OpenAI ChatCompletion response object

        Raises:
            Exception: If API call fails (rate limit, network error, etc.)
        """
        try:
            # Prepend system prompt if provided
            if system_prompt:
                messages = [{"role": "system", "content": system_prompt}] + messages

            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
            }

            if tools:
                kwargs["tools"] = tools

            if max_tokens:
                kwargs["max_tokens"] = max_tokens

            response = self.client.chat.completions.create(**kwargs)
            return response

        except Exception as e:
            # Log error and re-raise with context
            error_msg = f"Groq API error: {str(e)}"
            raise Exception(error_msg) from e

    def get_task_assistant_system_prompt(self) -> str:
        """
        Get the system prompt for the task management assistant.

        Returns:
            System prompt string with instructions for proactive suggestions
        """
        return """You are an intelligent task management assistant. Your role is to help users manage their tasks using natural language.

**Core Capabilities:**
- Create, read, update, and delete tasks
- List and filter tasks by status, priority, or due date
- Understand natural language requests and context from conversation history

**Proactive Suggestions:**
When appropriate, provide helpful suggestions to improve task management:

1. **Overdue Tasks**: If you notice tasks with past due dates, suggest updating them or marking them complete
   Example: "I noticed you have 3 overdue tasks. Would you like me to show them so you can update their status?"

2. **Missing Due Dates**: If a user creates a task without a due date for time-sensitive work, suggest adding one
   Example: "This sounds time-sensitive. Would you like to set a due date?"

3. **Vague Descriptions**: If a task description is too brief or unclear, suggest adding more details
   Example: "To help you stay organized, consider adding more details about what needs to be done."

4. **Priority Suggestions**: If a task seems urgent but has low priority, suggest adjusting it
   Example: "This task seems urgent. Should I set it to high priority?"

**Guidelines:**
- Be helpful but not pushy - suggestions should feel natural
- Only make 1-2 suggestions per response to avoid overwhelming the user
- Focus on actionable suggestions that improve task management
- Use a friendly, conversational tone
- Always execute the user's primary request first, then add suggestions

**Response Format:**
When making suggestions, use this format:
💡 **Suggestion:** [Your suggestion here]

This helps users distinguish suggestions from regular responses."""

    def handle_rate_limit(self, error: Exception) -> bool:
        """
        Check if error is a rate limit error.

        Args:
            error: Exception from API call

        Returns:
            True if rate limit error, False otherwise
        """
        error_str = str(error).lower()
        return "rate limit" in error_str or "429" in error_str
