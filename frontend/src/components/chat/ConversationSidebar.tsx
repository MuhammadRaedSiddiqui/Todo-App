/**
 * Conversation sidebar component for switching between conversations.
 */
'use client';

import { useEffect, useState } from 'react';
import { listConversations, deleteConversation } from '@/lib/chat-client';
import type { ConversationSummary } from '@/lib/types';

interface ConversationSidebarProps {
  currentConversationId?: number;
  onSelectConversation: (conversationId: number) => void;
  onNewConversation: () => void;
}

export function ConversationSidebar({
  currentConversationId,
  onSelectConversation,
  onNewConversation,
}: ConversationSidebarProps) {
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadConversations = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await listConversations(20, 0);
      setConversations(response.conversations);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load conversations');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadConversations();
  }, []);

  const handleDelete = async (conversationId: number, e: React.MouseEvent) => {
    e.stopPropagation();

    if (!confirm('Are you sure you want to delete this conversation?')) {
      return;
    }

    try {
      await deleteConversation(conversationId);
      setConversations((prev) => prev.filter((c) => c.id !== conversationId));

      // If deleting current conversation, start new one
      if (conversationId === currentConversationId) {
        onNewConversation();
      }
    } catch (err) {
      alert('Failed to delete conversation');
    }
  };

  return (
    <div className="w-64 border-r bg-gray-50 flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b bg-white">
        <button
          onClick={onNewConversation}
          className="w-full px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
        >
          + New Conversation
        </button>
      </div>

      {/* Conversation List */}
      <div className="flex-1 overflow-y-auto">
        {isLoading && (
          <div className="p-4 text-center text-gray-500">Loading...</div>
        )}

        {error && (
          <div className="p-4 text-center text-red-500 text-sm">{error}</div>
        )}

        {!isLoading && conversations.length === 0 && (
          <div className="p-4 text-center text-gray-500 text-sm">
            No conversations yet. Start a new one!
          </div>
        )}

        {conversations.map((conversation) => (
          <div
            key={conversation.id}
            onClick={() => onSelectConversation(conversation.id)}
            className={`p-3 border-b cursor-pointer hover:bg-gray-100 transition ${
              conversation.id === currentConversationId ? 'bg-blue-50 border-l-4 border-l-blue-500' : ''
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium text-gray-900 truncate">
                  {conversation.preview || 'New conversation'}
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  {conversation.message_count} messages
                </div>
                <div className="text-xs text-gray-400 mt-1">
                  {new Date(conversation.updated_at).toLocaleDateString()}
                </div>
              </div>
              <button
                onClick={(e) => handleDelete(conversation.id, e)}
                className="ml-2 text-gray-400 hover:text-red-500 transition"
                title="Delete conversation"
              >
                <svg
                  className="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                  />
                </svg>
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="p-3 border-t bg-white text-xs text-gray-500 text-center">
        {conversations.length} conversation{conversations.length !== 1 ? 's' : ''}
      </div>
    </div>
  );
}
