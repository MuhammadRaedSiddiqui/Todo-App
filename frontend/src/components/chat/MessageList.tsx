/**
 * Message list component for displaying chat messages.
 */
'use client';

import { useEffect, useRef } from 'react';
import type { Message } from '@/lib/types';
import { ToolCallDisplay } from './ToolCallDisplay';

interface MessageListProps {
  messages: Message[];
}

/**
 * Parse message content to detect and style suggestions.
 * Suggestions are formatted as: 💡 **Suggestion:** [text]
 */
function parseMessageContent(content: string) {
  const suggestionPattern = /💡\s*\*\*Suggestion:\*\*\s*(.+?)(?=\n💡|\n\n|$)/gs;
  const parts: Array<{ type: 'text' | 'suggestion'; content: string }> = [];
  let lastIndex = 0;

  let match;
  while ((match = suggestionPattern.exec(content)) !== null) {
    // Add text before suggestion
    if (match.index > lastIndex) {
      const textBefore = content.substring(lastIndex, match.index).trim();
      if (textBefore) {
        parts.push({ type: 'text', content: textBefore });
      }
    }

    // Add suggestion
    parts.push({ type: 'suggestion', content: match[1].trim() });
    lastIndex = match.index + match[0].length;
  }

  // Add remaining text
  if (lastIndex < content.length) {
    const remaining = content.substring(lastIndex).trim();
    if (remaining) {
      parts.push({ type: 'text', content: remaining });
    }
  }

  // If no suggestions found, return original content as text
  if (parts.length === 0) {
    parts.push({ type: 'text', content });
  }

  return parts;
}

export function MessageList({ messages }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        <div className="text-center">
          <p className="text-lg mb-2">👋 Hi! I'm your AI task assistant.</p>
          <p className="text-sm">
            Ask me to create, update, list, or delete your tasks using natural language.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 space-y-4">
      {messages.map((message) => {
        const contentParts = message.role === 'assistant'
          ? parseMessageContent(message.content)
          : [{ type: 'text' as const, content: message.content }];

        return (
          <div
            key={message.id}
            className={`flex ${
              message.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`max-w-[80%] rounded-lg p-3 ${
                message.role === 'user'
                  ? 'bg-blue-500 text-white'
                  : message.role === 'assistant'
                  ? 'bg-gray-100 text-gray-900'
                  : 'bg-yellow-50 text-gray-700 border border-yellow-200'
              }`}
            >
              {/* Role indicator */}
              <div className="text-xs font-semibold mb-1 opacity-70">
                {message.role === 'user'
                  ? 'You'
                  : message.role === 'assistant'
                  ? 'AI Assistant'
                  : 'Tool Execution'}
              </div>

              {/* Message content with suggestion styling */}
              <div className="space-y-2">
                {contentParts.map((part, index) => (
                  part.type === 'suggestion' ? (
                    <div
                      key={index}
                      className="mt-3 p-3 bg-blue-50 border-l-4 border-blue-400 rounded"
                    >
                      <div className="flex items-start">
                        <span className="text-xl mr-2">💡</span>
                        <div>
                          <div className="text-xs font-semibold text-blue-700 mb-1">
                            SUGGESTION
                          </div>
                          <div className="text-sm text-blue-900">
                            {part.content}
                          </div>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div key={index} className="whitespace-pre-wrap break-words">
                      {part.content}
                    </div>
                  )
                ))}
              </div>

              {/* Tool call display */}
              {message.role === 'tool' && message.tool_name && (
                <ToolCallDisplay
                  toolName={message.tool_name}
                  toolCallId={message.tool_call_id}
                />
              )}

              {/* Timestamp */}
              <div className="text-xs mt-2 opacity-60">
                {new Date(message.created_at).toLocaleTimeString()}
              </div>
            </div>
          </div>
        );
      })}
      <div ref={messagesEndRef} />
    </div>
  );
}
