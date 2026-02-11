/**
 * Main chat interface component using Vercel AI SDK.
 */
'use client';

import { useState, useEffect } from 'react';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import type { Message } from '@/lib/types';
import { sendChatMessage, getConversation } from '@/lib/chat-client';

interface ChatInterfaceProps {
  conversationId?: number;
  onConversationChange?: (conversationId: number) => void;
}

export function ChatInterface({ conversationId: initialConversationId, onConversationChange }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<number | undefined>(initialConversationId);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load conversation when conversationId changes
  useEffect(() => {
    if (initialConversationId && initialConversationId !== conversationId) {
      loadConversation(initialConversationId);
    }
  }, [initialConversationId]);

  const loadConversation = async (convId: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const conversation = await getConversation(convId);
      setMessages(conversation.messages);
      setConversationId(convId);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load conversation');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (content: string) => {
    if (!content.trim()) return;

    // Add user message to UI immediately
    const userMessage: Message = {
      id: Date.now(), // Temporary ID
      role: 'user',
      content,
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Send to backend
      const response = await sendChatMessage(content, conversationId);

      // Update conversation ID if new conversation
      if (!conversationId) {
        setConversationId(response.conversation_id);
        // Notify parent component of conversation change
        if (onConversationChange) {
          onConversationChange(response.conversation_id);
        }
      }

      // Add assistant response
      const assistantMessage: Message = {
        id: Date.now() + 1, // Temporary ID
        role: 'assistant',
        content: response.message,
        created_at: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');
      // Remove the optimistic user message on error
      setMessages((prev) => prev.slice(0, -1));
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewConversation = () => {
    setMessages([]);
    setConversationId(undefined);
    setError(null);
  };

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b">
        <h1 className="text-2xl font-bold">AI Task Assistant</h1>
        <button
          onClick={handleNewConversation}
          className="px-4 py-2 text-sm bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          New Conversation
        </button>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mx-4 mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto">
        <MessageList messages={messages} />
      </div>

      {/* Input */}
      <div className="border-t p-4">
        <MessageInput
          onSend={handleSendMessage}
          disabled={isLoading}
          placeholder="Ask me to manage your tasks..."
        />
      </div>

      {/* Loading Indicator */}
      {isLoading && (
        <div className="px-4 pb-2 text-sm text-gray-500">
          AI is thinking...
        </div>
      )}
    </div>
  );
}
