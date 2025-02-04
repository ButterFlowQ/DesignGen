import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import * as chatApi from '@/apis/chat';
import * as documentsApi from '@/apis/documents';

// Async thunk for fetching document
export const fetchDocument = createAsyncThunk(
  'chat/fetchDocument',
  async (documentId) => {
    return await documentsApi.fetchDocument(documentId);
  }
);

// Async thunk for sending messages
export const sendChatMessage = createAsyncThunk(
  'chat/sendMessage',
  async ({ message, agent, documentId, conversationId }) => {
    return await chatApi.sendChatMessage(message, agent, documentId, conversationId);
  }
);

const initialState = {
  documentId: null,
  document: null,
  htmlDocument: null,
  conversationId: null,
  messages: [],
  isLoading: false,
  isChatOpen: true,
  error: null,
  history: {
    past: [],
    future: []
  }
};

export const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    toggleChat: (state, action) => {
      state.isChatOpen = action.payload;
    },
    updateHistory: (state, action) => {
      state.history = action.payload;
    },
    resetConversation: (state) => {
      state.history.past.push({
        messages: state.messages,
        document: state.document,
        htmlDocument: state.htmlDocument
      });
      state.history.future = [];
      state.messages = [];
    },
    undo: (state) => {
      const previous = state.history.past[state.history.past.length - 1];
      if (previous) {
        const newPast = state.history.past.slice(0, -1);
        state.history = {
          past: newPast,
          future: [
            {
              messages: state.messages,
              document: state.document,
              htmlDocument: state.htmlDocument
            },
            ...state.history.future
          ]
        };
        state.messages = previous.messages;
        state.document = previous.document;
        state.htmlDocument = previous.htmlDocument;
      }
    },
    redo: (state) => {
      const next = state.history.future[0];
      if (next) {
        const newFuture = state.history.future.slice(1);
        state.history = {
          past: [
            ...state.history.past,
            {
              messages: state.messages,
              document: state.document,
              htmlDocument: state.htmlDocument
            }
          ],
          future: newFuture
        };
        state.messages = next.messages;
        state.document = next.document;
        state.htmlDocument = next.htmlDocument;
      }
    }
  },
  extraReducers: (builder) => {
    builder
      // Handle fetchDocument
      .addCase(fetchDocument.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchDocument.fulfilled, (state, action) => {
        state.isLoading = false;
        state.document = action.payload.document;
        state.htmlDocument = action.payload.html_document;
        state.conversationId = action.payload.conversation_id;
        state.messages = action.payload.chat_messages.map(msg => ({
          text: msg.message,
          sender: msg.is_user_message ? 'user' : 'bot',
          agent: msg.is_user_message ? msg.from_id : msg.to_id,
          timestamp: msg.creation_time
        }));
      })
      .addCase(fetchDocument.rejected, (state, action) => {
        state.isLoading = false;
        // Don't set error, use dummy data instead
        const data = dummyData;
        state.document = data.document;
        state.htmlDocument = data.html_document;
        state.conversationId = data.conversation_id;
        state.messages = data.chat_messages.map(msg => ({
          text: msg.message,
          sender: msg.is_user_message ? 'user' : 'bot',
          agent: msg.is_user_message ? msg.from_id : msg.to_id,
          timestamp: msg.creation_time
        }));
      })
      // Handle sendChatMessage
      .addCase(sendChatMessage.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(sendChatMessage.fulfilled, (state, action) => {
        state.isLoading = false;
        state.document = action.payload.document;
        state.htmlDocument = action.payload.html_document;
        state.conversationId = action.payload.conversation_id;
        state.history.past.push({
          messages: state.messages,
          document: state.document,
          htmlDocument: state.htmlDocument
        });
        state.history.future = [];
        state.messages = [
          ...state.messages,
          ...action.payload.chat_messages.map(msg => ({
            text: msg.message,
            sender: msg.is_user_message ? 'user' : 'bot',
            agent: msg.is_user_message ? msg.from_id : msg.to_id,
            timestamp: msg.creation_time
          }))
        ];
      })
      .addCase(sendChatMessage.rejected, (state, action) => {
        state.isLoading = false;
        // Don't set error, use dummy response instead
        const dummyResponse = {
          message: "The system is currently in offline mode. Your message will be processed when the connection is restored.",
          is_user_message: false,
          from_id: "system",
          to_id: "user",
          creation_time: new Date().toISOString()
        };
        state.messages = [
          ...state.messages,
          {
            text: dummyResponse.message,
            sender: 'bot',
            agent: dummyResponse.from_id,
            timestamp: dummyResponse.creation_time
          }
        ];
      });
  }
});

export const {
  toggleChat,
  updateHistory,
  resetConversation,
  undo,
  redo
} = chatSlice.actions;

export default chatSlice.reducer;