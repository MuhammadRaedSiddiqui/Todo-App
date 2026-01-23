/**
 * Chat page - AI Task Assistant interface with conversation sidebar.
 */
'use client';

import { useState } from 'react';
import { ChatInterface } from '@/components/chat/ChatInterface';
import { ConversationSidebar } from '@/components/chat/ConversationSidebar';

export default function ChatPage() {
  const [currentConversationId, setCurrentConversationId] = useState<number | undefined>();

  const handleSelectConversation = (conversationId: number) => {
    setCurrentConversationId(conversationId);
  };

  const handleNewConversation = () => {
    setCurrentConversationId(undefined);
  };

  const handleConversationChange = (conversationId: number) => {
    setCurrentConversationId(conversationId);
  };

  return (
    <div className="h-screen flex">
      <ConversationSidebar
        currentConversationId={currentConversationId}
        onSelectConversation={handleSelectConversation}
        onNewConversation={handleNewConversation}
      />
      <div className="flex-1">
        <ChatInterface
          conversationId={currentConversationId}
          onConversationChange={handleConversationChange}
        />
      </div>
    </div>
  );
}
