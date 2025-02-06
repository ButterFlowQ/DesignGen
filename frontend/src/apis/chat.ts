import { apiRequest } from './config';
import type { ChatMessage, Agent } from '@/types';


interface ChatMessageResponse {
  user_message: {
    message: string;
    to_id: string;
    is_user_message: boolean;
    creation_time: string;
  };
  agent_message: {
    message: string;
    from_id: string;
    is_user_message: boolean;
    creation_time: string;
  };
}

export async function fetchChatMessages(
  documentId: string,
  conversationId: string,
  page: number = 1
): Promise <ChatMessage[]> {
  return await apiRequest(
      `/orchestrator/chat/messages/?conversation_id=${conversationId}&page=${page}&document_id=${documentId}`);
}

export async function sendChatMessage(
  message: string,
  agent: Agent,
  conversationId: string,
  documentId: string
): Promise<ChatMessageResponse> {
  const userMessageData = {
    message,
    to_id: agent.id,
    is_user_message: true,
    conversation_id: conversationId,
    document_id: documentId
  };

  return await apiRequest(`/orchestrator/chat/messages/?conversation_id=${conversationId}`, {
    method: "POST",
    body: JSON.stringify(userMessageData)
  });
}