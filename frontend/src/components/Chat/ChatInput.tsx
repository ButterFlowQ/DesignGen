import { useRef, useEffect } from 'react';
import { Send, Loader2 } from 'lucide-react';
import type { ChatInputProps } from './types';

export function ChatInput({
  currentMessage,
  setCurrentMessage,
  selectedAgent,
  onAgentChange,
  onSendMessage,
  onKeyDown,
  agents,
  isLoading,
}: ChatInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 128)}px`;
    }
  }, [currentMessage]);

  return (
    <form onSubmit={onSendMessage} className="p-4 border-t bg-white">
      <div className="flex flex-col gap-2">
        <div className="relative">
          <select
            value={selectedAgent.id}
            onChange={onAgentChange}
            className="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg appearance-none pr-10
              focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
              disabled:opacity-50 disabled:cursor-not-allowed"
            title={selectedAgent.description}
            disabled={isLoading}
          >
            {agents.map(agent => (
              <option key={agent.id} value={agent.id}>
                {agent.name}
              </option>
            ))}
          </select>
          <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none">
            <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>
        
        <div className="flex items-end gap-2">
          <textarea
            ref={textareaRef}
            value={currentMessage}
            onChange={(e) => setCurrentMessage(e.target.value)}
            onKeyDown={onKeyDown}
            placeholder="Type your message... (Markdown supported)"
            className="flex-1 min-h-[2.5rem] max-h-32 px-3 py-2 bg-white border border-gray-300 rounded-lg resize-none
              focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
              disabled:opacity-50 disabled:cursor-not-allowed"
            rows={1}
            disabled={isLoading}
          />
          <button 
            type="submit" 
            className={`flex-shrink-0 p-2 bg-blue-600 text-white rounded-lg flex items-center justify-center
              hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
              disabled:opacity-50 disabled:cursor-not-allowed transition-colors
              h-10 w-10`}
            disabled={isLoading}
          >
            {isLoading ? (
              <Loader2 className="h-5 w-5 animate-spin" />
            ) : (
              <Send className="h-5 w-5" />
            )}
          </button>
        </div>
      </div>
    </form>
  );
}