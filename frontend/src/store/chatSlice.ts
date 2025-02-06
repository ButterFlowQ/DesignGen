import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import * as chatApi from '@/apis/chat';
import type { Message, Agent } from '@/types';
import { useAppDispatch } from '@/hooks/useAppDispatch';
import {
  fetchDocument,
} from '@/store/documentsSlice';

interface ChatState {
  messages: Message[];
  isLoading: boolean;
  isChatOpen: boolean;
  error: string | null;
  currentPage: number;
  totalPages: number;
}

interface SendMessagePayload {
  message: string;
  agent: Agent;
  conversationId: string;
  documentId: string;
}

const initialState: ChatState = {
  messages: [],
  isLoading: false,
  isChatOpen: true,
  error: null,
  currentPage: 1,
  totalPages: 1
};

// Async thunk for sending messages
export const sendChatMessage = createAsyncThunk(
  'chat/sendMessage',
  async ({ message, agent, conversationId, documentId }: SendMessagePayload, { dispatch }) => {
    try {
      const response = await chatApi.sendChatMessage(message, agent, conversationId, documentId);
      dispatch(fetchDocument(documentId));
      return response;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }
);

// Async thunk for fetching chat messages
export const fetchChatMessages = createAsyncThunk(
  'chat/fetchMessages',
  async ({ documentId, conversationId, page }: { documentId: string, conversationId: string; page: number }) => {
    console.log('fetchChatMessages', documentId, conversationId, page);
    return await chatApi.fetchChatMessages(documentId, conversationId, page);
  }
);

export const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    toggleChat: (state, action) => {
      state.isChatOpen = action.payload;
    },
    resetChat: (state) => {
      state.messages = [];
      state.currentPage = 1;
      state.totalPages = 1;
    }
  },
  extraReducers: (builder) => {
    builder
      // Handle sendChatMessage
      .addCase(sendChatMessage.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(sendChatMessage.fulfilled, (state, action) => {
        state.isLoading = false;
        const { user_message, agent_message } = action.payload;
        
        state.messages.push(
          {
            text: user_message.message,
            sender: 'user',
            agent: user_message.to_id,
            timestamp: user_message.creation_time
          },
          {
            text: agent_message.message,
            sender: 'bot',
            agent: agent_message.from_id,
            timestamp: agent_message.creation_time
          }
        );
      })
      .addCase(sendChatMessage.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to send message';
      })
      // Handle fetchChatMessages
      .addCase(fetchChatMessages.fulfilled, (state, action) => {
        console.log('fetchChatMessages', action.payload);
        state.messages = action.payload.map(msg => ({
          text: msg.message,
          sender: msg.is_user_message ? 'user' : 'bot',
          agent: msg.is_user_message ? msg.to_id : msg.from_id,
          timestamp: msg.creation_time
        }));
        console.log('fetchChatMessages', state.messages);
      });
  }
});

export const { toggleChat, resetChat } = chatSlice.actions;
export default chatSlice.reducer;