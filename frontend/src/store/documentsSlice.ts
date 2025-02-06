import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import * as documentsApi from '@/apis/documents';
import type { Document } from '@/types';
import { fetchChatMessages } from './chatSlice';

interface DocumentsState {
  documents: Document[];
  currentDocument: {
    id: string | null;
    title: string | null;
    document: any;
    htmlDocument: any;
    version: number | null;
    conversationId: string | null;
  };
  isLoading: boolean;
  error: string | null;
}

const initialState: DocumentsState = {
  documents: [],
  currentDocument: {
    id: null,
    title: null,
    document: null,
    htmlDocument: null,
    version: null,
    conversationId: null
  },
  isLoading: false,
  error: null
};

export const fetchDocuments = createAsyncThunk(
  'documents/fetchAll',
  async () => {
    return await documentsApi.fetchDocuments();
  }
);

export const fetchDocument = createAsyncThunk(
  'documents/fetchOne',
  async (documentId: string) => {
    const response = await documentsApi.fetchDocument(documentId);
    return response;
  }
);

export const createDocument = createAsyncThunk(
  'documents/create',
  async (title: string) => {
    return await documentsApi.createDocument(title);
  }
);

export const revertDocument = createAsyncThunk(
  'documents/revert',
  async ({ documentId, targetVersion }: { documentId: string; targetVersion: number }, {dispatch}) => {
    await documentsApi.revertDocument(documentId, targetVersion);
    const newDocument = await documentsApi.fetchDocument(documentId);
    dispatch(fetchChatMessages({documentId: documentId, conversationId: newDocument.conversation_id, page: 1}));
    return newDocument;
  }
);

const documentsSlice = createSlice({
  name: 'documents',
  initialState,
  reducers: {
    clearCurrentDocument: (state) => {
      state.currentDocument = initialState.currentDocument;
    }
  },
  extraReducers: (builder) => {
    builder
      // Fetch Documents List
      .addCase(fetchDocuments.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchDocuments.fulfilled, (state, action) => {
        state.isLoading = false;
        state.documents = action.payload;
      })
      .addCase(fetchDocuments.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch documents';
      })
      // Fetch Single Document
      .addCase(fetchDocument.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchDocument.fulfilled, (state, action) => {
        state.isLoading = false;
        state.currentDocument = {
          id: action.payload.id?.toString() || null,
          title: action.payload.title || null,
          document: action.payload.document_elements || null,
          htmlDocument: action.payload.html_elements || null,
          version: action.payload.version || null,
          conversationId: action.payload.conversation_id?.toString() || null
        };
      })
      .addCase(fetchDocument.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch document';
        // Keep the current document on error
        state.currentDocument = state.currentDocument;
      })
      // Create Document
      .addCase(createDocument.fulfilled, (state, action) => {
        state.documents.unshift(action.payload);
      })
      // Revert Document
      .addCase(revertDocument.fulfilled, (state, action) => {
        state.currentDocument = {
          id: action.payload.id?.toString() || null,
          title: action.payload.title || null,
          document: action.payload.document_elements || null,
          htmlDocument: action.payload.html_elements || null,
          version: action.payload.version || null,
          conversationId: action.payload.conversation_id?.toString() || null
        };
      });
  }
});

export const { clearCurrentDocument } = documentsSlice.actions;
export default documentsSlice.reducer;