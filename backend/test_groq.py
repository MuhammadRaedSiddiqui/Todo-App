"""Test script to verify Groq API connection."""
import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.groq_client import GroqClient


def test_groq_connection():
    """Test Groq API connection and basic chat completion."""
    print("Testing Groq API connection...")
    print("-" * 50)

    # Load environment variables
    load_dotenv()

    # Check if API key is set
    api_key = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your-groq-api-key-here":
        print("[ERROR] API key not set in .env file")
        print("Please add GROQ_API_KEY or OPENAI_API_KEY to backend/.env")
        return False

    try:
        # Initialize client
        print("[OK] Initializing Groq client...")
        client = GroqClient()
        print(f"  Base URL: {client.base_url}")
        print(f"  Model: {client.model}")

        # Test simple chat completion
        print("\n[OK] Testing chat completion...")
        messages = [
            {"role": "user", "content": "Say 'Hello from Groq!' if you can hear me."}
        ]

        response = client.chat_completion(messages=messages, temperature=0.7)

        # Extract response
        assistant_message = response.choices[0].message.content
        print(f"  Response: {assistant_message}")

        print("\n" + "=" * 50)
        print("[SUCCESS] Groq API connection verified!")
        print("=" * 50)
        return True

    except Exception as e:
        print("\n" + "=" * 50)
        print(f"[ERROR] {str(e)}")
        print("=" * 50)
        print("\nTroubleshooting:")
        print("1. Verify GROQ_API_KEY is correct in backend/.env")
        print("2. Check your internet connection")
        print("3. Verify Groq API status at https://status.groq.com")
        return False


if __name__ == "__main__":
    success = test_groq_connection()
    sys.exit(0 if success else 1)
