import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Search, Undo2, Redo2 } from 'lucide-react';
import { UserMenu } from './UserMenu';

interface NavbarProps {
  onUndo: () => void;
  onRedo: () => void;
  canUndo: boolean;
  canRedo: boolean;
}

function ButterflowLogo() {
  return (
    <svg
      width="32"
      height="32"
      viewBox="0 0 360 360"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M40 180 C40 180, 90 40, 180 180 S320 180, 320 180"
        fill="url(#butterflow-gradient)"
        strokeLinecap="round"
      />
      <defs>
        <linearGradient id="butterflow-gradient" x1="40" y1="180" x2="320" y2="180" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#FF9F43"/>
          <stop offset="100%" stopColor="#FFD32A"/>
        </linearGradient>
      </defs>
    </svg>
  );
}

export function Navbar({ onUndo, onRedo, canUndo, canRedo }: NavbarProps) {
  const navigate = useNavigate();

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const searchInput = e.currentTarget.querySelector('input');
    if (searchInput) {
      const query = searchInput.value.trim();
      if (query) {
        navigate(`/search?q=${encodeURIComponent(query)}`);
      }
    }
  };

  return (
    <nav className="bg-white shadow-md fixed top-0 left-0 right-0 z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Brand */}
          <Link 
            to="/" 
            className="flex items-center space-x-3 hover:opacity-80 transition-opacity"
          >
            <ButterflowLogo />
            <span className="font-bold text-xl text-gray-800">Butterflow</span>
          </Link>

          {/* Undo/Redo Controls */}
          <div className="flex items-center space-x-2">
            <button
              onClick={onUndo}
              disabled={!canUndo}
              className={`p-2 rounded-lg transition-all ${
                canUndo
                  ? 'text-orange-500 hover:bg-orange-50'
                  : 'text-gray-300 cursor-not-allowed'
              }`}
              title="Undo"
            >
              <Undo2 className="h-5 w-5" />
            </button>
            <button
              onClick={onRedo}
              disabled={!canRedo}
              className={`p-2 rounded-lg transition-all ${
                canRedo
                  ? 'text-orange-500 hover:bg-orange-50'
                  : 'text-gray-300 cursor-not-allowed'
              }`}
              title="Redo"
            >
              <Redo2 className="h-5 w-5" />
            </button>
          </div>

          {/* Search Bar and User Menu */}
          <div className="flex items-center space-x-4">
            <form onSubmit={handleSearch} className="hidden md:block relative">
              <input
                type="text"
                placeholder="Search..."
                className="w-64 pl-10 pr-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500"
              />
              <Search className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
            </form>
            <UserMenu />
          </div>
        </div>
      </div>
    </nav>
  );
}