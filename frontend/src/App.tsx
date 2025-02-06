import { Routes, Route } from 'react-router-dom';
import { Home, Document, NotFound, SignIn, SignUp } from './pages';
import { ProtectedRoute } from './components/ProtectedRoute';

function App() {
  return (
    <Routes>
      <Route 
        path="/" 
        element={
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/document/:documentId" 
        element={
          <ProtectedRoute>
            <Document />
          </ProtectedRoute>
        } 
      />
      <Route path="/signin" element={<SignIn />} />
      <Route path="/signup" element={<SignUp />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export default App;