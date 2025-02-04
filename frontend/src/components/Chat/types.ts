import type { Message, Agent } from '@/types';

export interface ChatProps {
  messages: Message[];
  onSendMessage: (message: string, agent: Agent) => void;
  onNewChat: () => void;
  isLoading: boolean;
  isChatOpen: boolean;
  onToggleChat: (value: boolean) => void;
  agents?: Agent[];
  className?: string;
}

export interface ChatInputProps {
  currentMessage: string;
  setCurrentMessage: (message: string) => void;
  selectedAgent: Agent;
  onAgentChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  onSendMessage: (e: React.FormEvent) => void;
  onKeyDown: (e: React.KeyboardEvent<HTMLTextAreaElement>) => void;
  agents: Agent[];
  isLoading: boolean;
}

export interface ChatMessageProps {
  message: Message;
}