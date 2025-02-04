import React, { useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { Chat } from '@/components/Chat';
import { Navbar } from '@/components/Navbar/Navbar';
import { DocumentRenderer } from '@/components/DocumentRenderer';
import { useAppDispatch } from '@/hooks/useAppDispatch';
import { useAppSelector } from '@/hooks/useAppSelector';
import { 
  fetchDocument, 
  sendChatMessage, 
  toggleChat, 
  resetConversation,
  undo, 
  redo 
} from '@/store/chatSlice';
import type { Agent } from '@/types';

export function Document() {
  const { documentId } = useParams<{ documentId: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useAppDispatch();
  const { 
    messages, 
    isLoading, 
    isChatOpen, 
    history,
    document,
    htmlDocument,
    conversationId
  } = useAppSelector(state => state.chat);

  useEffect(() => {
    // Validate documentId and redirect if invalid
    if (!documentId || isNaN(Number(documentId))) {
      navigate('/404', { replace: true });
      return;
    }
    
    dispatch(fetchDocument(documentId));
  }, [documentId, dispatch, navigate]);

  const handleSendMessage = async (message: string, agent: Agent) => {
    if (documentId && conversationId) {
      dispatch(sendChatMessage({
        message,
        agent,
        documentId,
        conversationId
      }));
    }
  };

  const handleNewChat = () => {
    // Update URL to remove any chat-related parameters
    navigate(location.pathname, { replace: true });
    dispatch(resetConversation());
  };

  const handleToggleChat = (value: boolean) => {
    // Update URL to reflect chat state
    const searchParams = new URLSearchParams(location.search);
    if (value) {
      searchParams.set('chat', 'open');
    } else {
      searchParams.delete('chat');
    }
    navigate(`${location.pathname}?${searchParams.toString()}`, { replace: true });
    
    dispatch(toggleChat(value));
  };

  if (isLoading && !messages.length) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading document...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar 
        onUndo={() => dispatch(undo())} 
        onRedo={() => dispatch(redo())}
        canUndo={history.past.length > 0}
        canRedo={history.future.length > 0}
      />
      <div className={`pt-16 transition-all duration-300 ${isChatOpen ? 'sm:mr-[50%] lg:mr-[30%]' : 'mr-12'}`}>
        <div className="max-w-4xl mx-auto px-4 py-8">
          <DocumentRenderer 
            document={document} 
            htmlDocument={htmlDocument} 
          />
        </div>
      </div>
      
      <Chat
        messages={messages}
        onSendMessage={handleSendMessage}
        onNewChat={handleNewChat}
        isLoading={isLoading}
        isChatOpen={isChatOpen}
        onToggleChat={handleToggleChat}
      />
    </div>
  );
}