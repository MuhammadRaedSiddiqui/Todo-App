"""Direct test of chat service to see actual errors."""
import sys
import os
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

load_dotenv()

from src.services.chat_service import chat_service
from src.core.database import get_session

def test_chat():
    """Test chat service directly."""
    print("Testing chat service...")

    # Get database session
    session = next(get_session())

    try:
        # Test with user_id 5 (the test user we logged in with)
        result = chat_service.process_message(
            user_message="Create a task to buy groceries tomorrow",
            user_id=5,
            session=session,
            conversation_id=None
        )

        print("\n=== SUCCESS ===")
        print(f"Result: {result}")

    except Exception as e:
        print("\n=== ERROR ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        session.close()

if __name__ == "__main__":
    test_chat()
