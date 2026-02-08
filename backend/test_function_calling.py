"""Test Groq function calling capability."""
from src.services.groq_client import GroqClient

def test_function_calling():
    """Test if Groq properly supports function calling."""
    client = GroqClient()

    # Simple test tool
    tools = [{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name"
                    }
                },
                "required": ["location"]
            }
        }
    }]

    messages = [
        {"role": "user", "content": "What's the weather in Paris?"}
    ]

    print("Testing Groq function calling...")
    print(f"Model: {client.model}")
    print(f"Tools: {tools}")
    print()

    try:
        response = client.chat_completion(
            messages=messages,
            tools=tools,
            temperature=0.7
        )

        message = response.choices[0].message

        print("=== RESPONSE ===")
        print(f"Has tool_calls attribute: {hasattr(message, 'tool_calls')}")
        print(f"tool_calls value: {getattr(message, 'tool_calls', None)}")
        print(f"Content: {message.content}")
        print(f"Full message object: {message}")

        if message.tool_calls:
            print("\n✅ Function calling IS working!")
            for tool_call in message.tool_calls:
                print(f"  - Tool: {tool_call.function.name}")
                print(f"  - Args: {tool_call.function.arguments}")
        else:
            print("\n❌ Function calling NOT working - AI returned text instead")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_function_calling()
