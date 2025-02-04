import React from 'react';
import { Link } from 'react-router-dom';
import { FileText, ArrowRight } from 'lucide-react';
import type { Document } from '@/types';

interface DocumentListProps {
  documents: Document[];
  isLoading: boolean;
  searchQuery: string;
}

export function DocumentList({ documents, isLoading, searchQuery }: DocumentListProps) {
  const filteredDocuments = documents.filter(doc =>
    doc.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (isLoading) {
    return (
      <div className="px-4 py-6 sm:py-8 text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
        <p className="mt-2 text-sm text-gray-500">Loading documents...</p>
      </div>
    );
  }

  if (filteredDocuments.length === 0) {
    return (
      <div className="px-4 py-6 sm:py-8 text-center text-gray-500 text-sm sm:text-base">
        {searchQuery ? 'No documents found matching your search.' : 'No documents yet. Create your first one!'}
      </div>
    );
  }

  return (
    <>
      {filteredDocuments.map((doc) => (
        <Link
          key={doc.id}
          to={`/document/${doc.id}`}
          className="block hover:bg-gray-50 transition-colors duration-150"
        >
          <div className="px-4 py-3 sm:py-4 flex items-center">
            <div className="flex-shrink-0">
              <div className="p-2 bg-blue-100 rounded-lg">
                <FileText className="h-5 w-5 sm:h-6 sm:w-6 text-blue-600" />
              </div>
            </div>
            <div className="ml-3 sm:ml-4 flex-1 min-w-0">
              <h3 className="text-base sm:text-lg font-medium text-gray-900 truncate">
                {doc.title}
              </h3>
              <p className="text-xs sm:text-sm text-gray-500 mt-0.5">
                Last edited {new Date(doc.lastEdited).toLocaleDateString()} at{' '}
                {new Date(doc.lastEdited).toLocaleTimeString()}
              </p>
            </div>
            <ArrowRight className="h-4 w-4 sm:h-5 sm:w-5 text-gray-400 flex-shrink-0" />
          </div>
        </Link>
      ))}
    </>
  );
}