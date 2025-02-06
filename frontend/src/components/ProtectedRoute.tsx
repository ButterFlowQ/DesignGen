import { Navigate, useLocation } from 'react-router-dom';
import { useAppSelector } from '@/hooks';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated } = useAppSelector(state => state.auth);
  const location = useLocation();

  if (!isAuthenticated) {
    // Redirect to signin page while saving the attempted URL
    return <Navigate to="/signin" state={{ from: location }} replace />;
  }

  return <>{children}</>;
}