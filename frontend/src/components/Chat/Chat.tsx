import React from 'react';
import { MessageSquare, ChevronLeft, Plus, X } from 'lucide-react';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import type { ChatProps } from './types';
import type { Agent } from '@/types';

const defaultAgents: Agent[] = [
  { id: "1", name: "Functional Requirement" },
  { id: "2", name: "Non functional Requirement" },
  { id: "3", name: "Architecture" },
  { id: "4", name: "Api Contract" },
  { id: "5", name: "Database Schema" },
  { id: "6", name: "Java LLD" },
  { id: "7", name: "Java Code" },
  { id: "8", name: "React LLD" },
  { id: "9", name: "React Code" }
];

export function Chat({ 
  agents = defaultAgents,
  messages,
  onSendMessage,
  onNewChat,
  isLoading,
  className = '',
  isChatOpen,
  onToggleChat
}: ChatProps) {
  const [currentMessage, setCurrentMessage] = React.useState('');
  const [selectedAgent, setSelectedAgent] = React.useState<Agent>(agents[0]);
  const messagesEndRef = React.useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  React.useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (currentMessage.trim() && !isLoading) {
      try {
        await onSendMessage(currentMessage, selectedAgent);
        setCurrentMessage('');
      } catch (error) {
        console.error('Error sending message:', error);
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  const handleNewConversation = () => {
    onNewChat?.();
    setCurrentMessage('');
  };

  const handleAgentChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newAgent = agents.find(agent => agent.id === e.target.value) || agents[0];
    setSelectedAgent(newAgent);
  };

  return (
    <div 
      className={`fixed top-16 right-0 h-[calc(100%-4rem)] bg-white shadow-lg transition-all duration-300 z-40
        ${isChatOpen ? 'w-full sm:w-1/2 lg:w-[30%]' : 'w-0 sm:w-12'} ${className}`}
    >
      <button
        onClick={() => onToggleChat(!isChatOpen)}
        className={`hidden sm:block absolute left-0 top-1/2 -translate-x-full -translate-y-1/2 bg-white p-2 shadow-lg rounded-l-lg
          hover:bg-gray-50 transition-colors`}
      >
        <ChevronLeft className={`h-5 w-5 text-gray-500 transition-transform ${isChatOpen ? 'rotate-180' : ''}`} />
      </button>

      {isChatOpen && (
        <div className="flex flex-col h-full">
          <div className="p-4 border-b flex items-center justify-between bg-white">
            <div className="flex items-center gap-2">
              <MessageSquare className="h-5 w-5 text-blue-500" />
              <h2 className="font-semibold text-gray-900">Chat Support</h2>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={handleNewConversation}
                className="flex items-center gap-2 px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Plus className="h-4 w-4" />
                <span className="hidden sm:inline">New Chat</span>
              </button>
              <button
                onClick={() => onToggleChat(false)}
                className="sm:hidden p-2 hover:bg-gray-100 rounded-lg transition-colors"
                aria-label="Close chat"
              >
                <X className="h-5 w-5 text-gray-500" />
              </button>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto bg-gray-50 p-4">
            {messages.map((message, index) => (
              <ChatMessage 
                key={`${message.timestamp}-${message.sender}-${index}`} 
                message={message} 
              />
            ))}
            <div ref={messagesEndRef} />
          </div>

          <ChatInput
            currentMessage={currentMessage}
            setCurrentMessage={setCurrentMessage}
            selectedAgent={selectedAgent}
            onAgentChange={handleAgentChange}
            onSendMessage={handleSendMessage}
            onKeyDown={handleKeyDown}
            agents={agents}
            isLoading={isLoading}
          />
        </div>
      )}
    </div>
  );
}