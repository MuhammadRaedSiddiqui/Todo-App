"""Conversation management API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from src.core.database import get_session
from src.api.dependencies import get_current_user
from src.models.conversation import Conversation
from src.models.message import Message


router = APIRouter(prefix="/api/chat/conversations", tags=["conversations"])


class ConversationSummary(BaseModel):
    """Summary of a conversation for list view."""
    id: int
    created_at: datetime
    updated_at: datetime
    message_count: int
    preview: Optional[str] = None


class ConversationListResponse(BaseModel):
    """Response model for conversation list."""
    conversations: List[ConversationSummary]
    total: int


class MessageResponse(BaseModel):
    """Response model for a message."""
    id: int
    role: str
    content: str
    tool_call_id: Optional[str] = None
    tool_name: Optional[str] = None
    created_at: datetime


class ConversationDetailResponse(BaseModel):
    """Response model for conversation with messages."""
    id: int
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse]


@router.get("", response_model=ConversationListResponse)
async def list_conversations(
    limit: int = 20,
    offset: int = 0,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """
    List all conversations for the authenticated user.

    Args:
        limit: Maximum number of conversations to return
        offset: Number of conversations to skip
        session: Database session
        current_user: Authenticated user from JWT

    Returns:
        ConversationListResponse with list of conversations
    """
    # Query conversations for user
    query = (
        select(Conversation)
        .where(Conversation.user_id == current_user["id"])
        .order_by(Conversation.updated_at.desc())
        .offset(offset)
        .limit(limit)
    )

    conversations = session.exec(query).all()

    # Build response with message counts and previews
    conversation_summaries = []
    for conv in conversations:
        # Get message count
        message_count = len(conv.messages)

        # Get first user message as preview
        preview = None
        if conv.messages:
            first_user_msg = next(
                (msg for msg in conv.messages if msg.role == "user"),
                None
            )
            if first_user_msg:
                preview = first_user_msg.content[:100]

        conversation_summaries.append(
            ConversationSummary(
                id=conv.id,
                created_at=conv.created_at,
                updated_at=conv.updated_at,
                message_count=message_count,
                preview=preview
            )
        )

    # Get total count
    total_query = select(Conversation).where(
        Conversation.user_id == current_user["id"]
    )
    total = len(session.exec(total_query).all())

    return ConversationListResponse(
        conversations=conversation_summaries,
        total=total
    )


@router.get("/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    conversation_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific conversation with all messages.

    Args:
        conversation_id: ID of the conversation
        session: Database session
        current_user: Authenticated user from JWT

    Returns:
        ConversationDetailResponse with conversation and messages

    Raises:
        HTTPException: If conversation not found or access denied
    """
    # Get conversation
    conversation = session.get(Conversation, conversation_id)

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    # Verify ownership
    if conversation.user_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this conversation"
        )

    # Get messages
    query = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )
    messages = session.exec(query).all()

    message_responses = [
        MessageResponse(
            id=msg.id,
            role=msg.role,
            content=msg.content,
            tool_call_id=msg.tool_call_id,
            tool_name=msg.tool_name,
            created_at=msg.created_at
        )
        for msg in messages
    ]

    return ConversationDetailResponse(
        id=conversation.id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        messages=message_responses
    )


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a conversation and all its messages.

    Args:
        conversation_id: ID of the conversation to delete
        session: Database session
        current_user: Authenticated user from JWT

    Raises:
        HTTPException: If conversation not found or access denied
    """
    # Get conversation
    conversation = session.get(Conversation, conversation_id)

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    # Verify ownership
    if conversation.user_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this conversation"
        )

    # Delete conversation (cascade will delete messages)
    session.delete(conversation)
    session.commit()

    return None
