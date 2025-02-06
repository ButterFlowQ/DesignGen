import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch } from '@/hooks';
import { createDocument } from '@/store/documentsSlice';

interface CreateDocumentFormProps {
  isOpen: boolean;
  onClose: () => void;
}

export function CreateDocumentForm({ isOpen, onClose }: CreateDocumentFormProps) {
  const [title, setTitle] = React.useState('');
  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (title.trim()) {
      const resultAction = await dispatch(createDocument(title));
      if (createDocument.fulfilled.match(resultAction)) {
        navigate(`/document/${resultAction.payload.id}`);
      }
    }
  };

  if (!isOpen) return null;

  return (
    <form onSubmit={handleSubmit} className="mb-6 sm:mb-8 bg-white p-4 rounded-lg shadow-sm">
      <div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
        <input
          type="text"
          placeholder="Enter document title..."
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          autoFocus
        />
        <div className="flex gap-2 sm:gap-3">
          <button
            type="submit"
            className="flex-1 sm:flex-none px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
          >
            Create
          </button>
          <button
            type="button"
            onClick={() => {
              setTitle('');
              onClose();
            }}
            className="flex-1 sm:flex-none px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    </form>
  );
}