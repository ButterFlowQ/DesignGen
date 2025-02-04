import { apiRequest } from './config';
import { dummyData } from './dummyData';
import type { Document } from '@/types';

export async function fetchDocuments(): Promise<Document[]> {
  // TODO: Replace with actual API call
  await new Promise(resolve => setTimeout(resolve, 500));
  
  const mockDocuments: Document[] = [
    { 
      id: '1', 
      title: 'Project Requirements', 
      lastEdited: new Date().toISOString(),
      createdBy: '1'
    },
    { 
      id: '2', 
      title: 'API Documentation', 
      lastEdited: new Date(Date.now() - 86400000).toISOString(),
      createdBy: '1'
    },
    { 
      id: '3', 
      title: 'System Architecture', 
      lastEdited: new Date(Date.now() - 259200000).toISOString(),
      createdBy: '1'
    }
  ];
  return mockDocuments;
}

export async function createDocument(title: string): Promise<Document> {
  // TODO: Replace with actual API call
  await new Promise(resolve => setTimeout(resolve, 500));
  
  return {
    id: String(Date.now()),
    title,
    lastEdited: new Date().toISOString(),
    createdBy: '1'
  };
}

export async function fetchDocument(documentId: string) {
  try {
    return await apiRequest(
      `/orchestrator/get_document/${documentId}`,
      { mode: "cors" }
    );
  } catch (error) {
    console.warn('API Error:', error);
    return dummyData; // Return dummy data on error
  }
}