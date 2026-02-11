"""Create conversations and messages tables for AI chatbot

Revision ID: 003
Revises: 002
Create Date: 2026-01-18
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '003'
down_revision = '002'  # Previous migration from Phase 2
branch_labels = None
depends_on = None


def upgrade():
    """Create conversations and messages tables."""
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('idx_conversations_updated_at', 'conversations', ['updated_at'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_call_id', sa.String(length=100), nullable=True),
        sa.Column('tool_name', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("role IN ('user', 'assistant', 'tool')", name='check_message_role'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('idx_messages_created_at', 'messages', ['created_at'])


def downgrade():
    """Drop conversations and messages tables."""
    op.drop_index('idx_messages_created_at', table_name='messages')
    op.drop_index('idx_messages_conversation_id', table_name='messages')
    op.drop_table('messages')

    op.drop_index('idx_conversations_updated_at', table_name='conversations')
    op.drop_index('idx_conversations_user_id', table_name='conversations')
    op.drop_table('conversations')
