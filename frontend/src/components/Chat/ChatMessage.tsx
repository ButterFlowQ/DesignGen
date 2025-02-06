import React from 'react';
import ReactMarkdown from 'react-markdown';
import type { ChatMessageProps } from './types';

export function ChatMessage({ message }: ChatMessageProps) {
  const timestamp = new Date(message.timestamp);
  
  return (
    <div className={`mb-3 flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-[85%] rounded-lg p-2.5 ${
        message.sender === 'user' 
          ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white shadow-sm' 
          : 'bg-white text-gray-900 shadow-sm'
      }`}>
        <ReactMarkdown 
          className={`whitespace-pre-wrap text-sm prose prose-sm max-w-none ${
            message.sender === 'user' 
              ? 'prose-invert prose-p:text-white/90 prose-headings:text-white prose-code:text-white/80' 
              : ''
          }`}
          components={{
            p: ({ children }) => <p className="text-sm leading-relaxed mb-1 last:mb-0">{children}</p>,
            h1: ({ children }) => <h1 className="text-base font-bold mb-1">{children}</h1>,
            h2: ({ children }) => <h2 className="text-sm font-bold mb-1">{children}</h2>,
            h3: ({ children }) => <h3 className="text-sm font-semibold mb-1">{children}</h3>,
            ul: ({ children }) => <ul className="text-sm list-disc pl-4 mb-1">{children}</ul>,
            ol: ({ children }) => <ol className="text-sm list-decimal pl-4 mb-1">{children}</ol>,
            li: ({ children }) => <li className="mb-0.5">{children}</li>,
            code: ({ children }) => (
              <code className={`text-xs rounded px-1 py-0.5 ${
                message.sender === 'user' 
                  ? 'bg-white/20' 
                  : 'bg-gray-100'
              }`}>
                {children}
              </code>
            ),
            pre: ({ children }) => (
              <pre className={`text-xs rounded p-2 my-1 overflow-x-auto ${
                message.sender === 'user' 
                  ? 'bg-white/20' 
                  : 'bg-gray-100'
              }`}>
                {children}
              </pre>
            ),
          }}
        >
          {message.text}
        </ReactMarkdown>
        <span className={`block mt-1 text-[10px] ${
          message.sender === 'user' 
            ? 'text-white/70' 
            : 'text-gray-500'
        }`}>
          {timestamp.toLocaleTimeString()}
        </span>
      </div>
    </div>
  );
}