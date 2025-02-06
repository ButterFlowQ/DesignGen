import { useState } from 'react';
import { Search, Plus, Clock } from 'lucide-react';
import { UserMenu } from '@/components/Navbar/UserMenu';
import { DocumentList } from '@/components/Documents/DocumentList';
import { CreateDocumentForm } from '@/components/Documents/CreateDocumentForm';
import { useDocuments } from '@/hooks/useDocuments';
import { ButterflowLogo } from '@/components/ButterflowLogo';

export function Home() {
  const [searchQuery, setSearchQuery] = useState('');
  const [isCreatingDoc, setIsCreatingDoc] = useState(false);
  const { documents, isLoading } = useDocuments();

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      {/* User Menu */}
      <div className="absolute top-4 right-4 z-50">
        <UserMenu />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="py-8 sm:py-12 md:py-16 lg:py-20">
          {/* Header Section */}
          <div className="text-center">
            <div className="flex justify-center mb-4 sm:mb-6">
              <ButterflowLogo />
            </div>
            <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-extrabold text-gray-900">
              <span className="block">Document Management</span>
              <span className="block text-blue-500 mt-2">Made Simple</span>
            </h1>
            <p className="mt-3 max-w-md mx-auto text-sm sm:text-base md:text-lg lg:text-xl text-gray-500 md:mt-5 md:max-w-3xl">
              Access, manage, and collaborate on your documents with our intuitive platform.
            </p>
          </div>

          {/* Search and Create Section */}
          <div className="mt-8 sm:mt-12 max-w-3xl mx-auto">
            <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 mb-6 sm:mb-8">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search documents..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 sm:py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <button
                onClick={() => setIsCreatingDoc(true)}
                className="flex items-center justify-center px-4 py-2 sm:py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
              >
                <Plus className="h-5 w-5 mr-2" />
                <span>New Document</span>
              </button>
            </div>

            <CreateDocumentForm 
              isOpen={isCreatingDoc} 
              onClose={() => setIsCreatingDoc(false)} 
            />

            {/* Documents List */}
            <div className="bg-white rounded-lg shadow-sm overflow-hidden">
              <div className="px-4 py-3 border-b border-gray-200">
                <div className="flex items-center text-gray-500">
                  <Clock className="h-5 w-5 mr-2" />
                  <span className="text-sm sm:text-base">Recent Documents</span>
                </div>
              </div>
              <div className="divide-y divide-gray-200">
                <DocumentList 
                  documents={documents}
                  isLoading={isLoading}
                  searchQuery={searchQuery}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}