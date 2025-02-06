import { apiRequest } from './config';
import type { Document } from '@/types';

interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

interface CreateDocumentResponse {
  document_id: number;
  versioned_document_id: number;
}

interface DocumentDetailsResponse {
  id: number;
  latest_version: number;
  title: string;
  version: number;
  document_elements: any;
  html_elements: any;
  creation_time: string;
  conversation_id: string;
}

interface DocumentResponse {
  id: number;
  title: string;
  last_modified: string;
}

export async function fetchDocuments(): Promise<Document[]> {
  const response = await apiRequest<PaginatedResponse<DocumentResponse>>('/orchestrator/documents/');
  return response.results.map((doc) => ({
    id: doc.id.toString(),
    title: doc.title,
    lastEdited: doc.last_modified,
  }));
}

export async function createDocument(title: string): Promise<Document> {
  const response = await apiRequest<CreateDocumentResponse>('/orchestrator/documents/', {
    method: 'POST',
    body: JSON.stringify({
      document_schema_id: 1,
      title
    })
  });

  return {
    id: response.document_id.toString(),
    title,
    lastEdited: new Date().toISOString(),
  };
}

export async function fetchDocument(documentId: string): Promise<DocumentDetailsResponse> {
  return await apiRequest(`/orchestrator/documents/${documentId}/`);
}

export async function revertDocument(documentId: string, targetVersion: number): Promise<void> {
  await apiRequest(`/orchestrator/documents/${documentId}/revert/`, {
    method: 'POST',
    body: JSON.stringify({
      target_version: targetVersion
    })
  });
}