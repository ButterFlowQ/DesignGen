import { apiRequest } from './config';
import { dummyData } from './dummyData';
import type { Agent } from '@/types';

export async function sendChatMessage(
  message: string,
  agent: Agent,
  documentId: string,
  conversationId: string
) {
  try {
    return await apiRequest('/orchestrator/send_chat_message/', {
      method: "POST",
      body: JSON.stringify({
        message,
        from_id: "1", // User ID
        to_id: agent.id,
        document_id: documentId,
        conversation_id: conversationId,
      }),
      mode: "cors",
    });
  } catch (error) {
    console.warn('API Error:', error);
    // Return dummy response on error
    return {
      chat_messages: [
        {
          id: Date.now(),
          message,
          from_id: null,
          to_id: agent.id,
          is_user_message: true,
          creation_time: new Date().toISOString()
        },
        {
          id: Date.now() + 1,
          message: "I understand your message. However, I'm currently in offline mode due to API unavailability. I'll be fully functional once the connection is restored.",
          from_id: agent.id,
          to_id: null,
          is_user_message: false,
          creation_time: new Date().toISOString()
        }
      ],
      conversation_id: conversationId,
      document: dummyData.document
    };
  }
}