"""Chat API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import BaseModel
from typing import Optional

from src.core.database import get_session
from src.api.dependencies import get_current_user
from src.services.chat_service import chat_service


router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatMessageRequest(BaseModel):
    """Request model for sending a chat message."""
    message: str
    conversation_id: Optional[int] = None


class ChatMessageResponse(BaseModel):
    """Response model for chat message."""
    message: str
    conversation_id: int
    role: str


@router.post("/message", response_model=ChatMessageResponse)
async def send_chat_message(
    request: ChatMessageRequest,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Send a chat message and receive AI response.

    Args:
        request: Chat message request with message and optional conversation_id
        session: Database session
        current_user: Authenticated user from JWT

    Returns:
        ChatMessageResponse with AI response

    Raises:
        HTTPException: If message is empty or conversation access denied
    """
    # Validate input
    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )

    # Sanitize input
    sanitized_message = chat_service.sanitize_input(request.message)

    try:
        # Process message
        result = chat_service.process_message(
            user_message=sanitized_message,
            user_id=current_user.id,
            session=session,
            conversation_id=request.conversation_id
        )

        return ChatMessageResponse(**result)

    except ValueError as e:
        # Conversation not found or access denied
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        # Internal error - log for debugging
        import traceback
        print(f"ERROR in chat endpoint: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
