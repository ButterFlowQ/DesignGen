import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import * as documentsApi from '@/apis/documents';
import type { Document } from '@/types';

interface DocumentsState {
  documents: Document[];
  isLoading: boolean;
  error: string | null;
}

const initialState: DocumentsState = {
  documents: [],
  isLoading: false,
  error: null
};

export const fetchDocuments = createAsyncThunk(
  'documents/fetchAll',
  async () => {
    return await documentsApi.fetchDocuments();
  }
);

export const createDocument = createAsyncThunk(
  'documents/create',
  async (title: string) => {
    return await documentsApi.createDocument(title);
  }
);

const documentsSlice = createSlice({
  name: 'documents',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      // Fetch Documents
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
      // Create Document
      .addCase(createDocument.fulfilled, (state, action) => {
        state.documents.unshift(action.payload);
      });
  }
});

export default documentsSlice.reducer;