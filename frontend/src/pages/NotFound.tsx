import { Link } from 'react-router-dom';
import { Home as HomeIcon } from 'lucide-react';

export function NotFound() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center px-4">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-gray-900">404</h1>
        <h2 className="mt-3 text-2xl font-semibold text-gray-700">Page not found</h2>
        <p className="mt-4 text-gray-500">The page you're looking for doesn't exist or has been moved.</p>
        
        <Link 
          to="/" 
          className="mt-6 inline-flex items-center px-4 py-2 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <HomeIcon className="h-5 w-5 mr-2" />
          Back to Home
        </Link>
      </div>
    </div>
  );
}