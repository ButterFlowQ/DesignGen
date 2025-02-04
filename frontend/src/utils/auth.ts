// Dummy JWT token generation
export function generateDummyToken(userId: string): string {
  return `dummy_jwt_token_${userId}_${Date.now()}`;
}

// Store token in localStorage
export function setAuthToken(token: string): void {
  localStorage.setItem('auth_token', token);
}

// Get token from localStorage
export function getAuthToken(): string | null {
  return localStorage.getItem('auth_token');
}

// Remove token from localStorage
export function removeAuthToken(): void {
  localStorage.removeItem('auth_token');
}

// Add auth header to API requests
export function getAuthHeaders(): HeadersInit {
  const token = getAuthToken();
  return token ? {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  } : {
    'Content-Type': 'application/json'
  };
}