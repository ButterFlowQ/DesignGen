import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Chat } from '@/components/Chat';
import { Navbar } from '@/components/Navbar/Navbar';
import { DocumentRenderer } from '@/components/DocumentRenderer';
import { useAppDispatch } from '@/hooks/useAppDispatch';
import { useAppSelector } from '@/hooks/useAppSelector';
import { 
  sendChatMessage, 
  toggleChat, 
  resetChat,
  fetchChatMessages
} from '@/store/chatSlice';
import {
  fetchDocument,
  revertDocument
} from '@/store/documentsSlice';
import type { Agent } from '@/types';

export function Document() {
  const { documentId } = useParams<{ documentId: string }>();
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  
  const { 
    messages, 
    isLoading: isChatLoading, 
    isChatOpen
  } = useAppSelector(state => state.chat);

  const {
    currentDocument,
    isLoading: isDocumentLoading
  } = useAppSelector(state => state.documents);

  useEffect(() => {
    // Validate documentId and redirect if invalid
    if (!documentId || isNaN(Number(documentId))) {
      navigate('/404', { replace: true });
      return;
    }
    
    dispatch(fetchDocument(documentId));
  }, [documentId, dispatch, navigate]);

  // Fetch chat messages when conversation ID is available
  useEffect(() => {
    if (documentId && currentDocument.conversationId) {
      dispatch(fetchChatMessages({ 
        documentId,
        conversationId: currentDocument.conversationId,
        page: 1
      }));
    }
  }, [documentId, currentDocument.conversationId, dispatch]);

  const handleSendMessage = async (message: string, agent: Agent) => {
    if (documentId) {
      dispatch(sendChatMessage({
        message,
        agent,
        conversationId: currentDocument.conversationId,
        documentId
      }));
    }
  };

  const handleNewChat = () => {
    dispatch(resetChat());
  };

  const handleToggleChat = (value: boolean) => {
    dispatch(toggleChat(value));
  };

  const handleUndo = () => {
    if (documentId && currentDocument.version) {
      const targetVersion = currentDocument.version - 1;
      if (targetVersion > 0) {
        dispatch(revertDocument({ documentId, targetVersion }));
      }
    }
  };


  if (isDocumentLoading && !messages.length) {
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
        onUndo={handleUndo}
        canUndo={currentDocument.version ? currentDocument.version > 1 : false}
      />
      <div className={`pt-16 transition-all duration-300 ${isChatOpen ? 'sm:mr-[50%] lg:mr-[30%]' : 'mr-12'}`}>
        <div className="max-w-4xl mx-auto px-4 py-8">
          {currentDocument.title && (
            <h1 className="text-3xl font-bold text-gray-900 mb-6">{currentDocument.title}</h1>
          )}
          <DocumentRenderer 
            document={currentDocument.document} 
            htmlDocument={currentDocument.htmlDocument} 
          />
        </div>
      </div>
      
      <Chat
        messages={messages}
        onSendMessage={handleSendMessage}
        onNewChat={handleNewChat}
        isLoading={isChatLoading}
        isChatOpen={isChatOpen}
        onToggleChat={handleToggleChat}
      />
    </div>
  );
}