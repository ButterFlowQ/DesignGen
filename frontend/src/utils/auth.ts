import Cookies from 'js-cookie';

const TOKEN_KEY = 'auth_token';
const USER_KEY = 'auth_user';
const COOKIE_EXPIRES = 7; // Cookie expiration in days

interface StoredUser {
  id: string;
  name: string;
  email: string;
  avatarUrl: string;
}

// Store token in both cookie and localStorage for better persistence
export function setAuthToken(token: string): void {
  // Set in cookie with expiration
  Cookies.set(TOKEN_KEY, token, {
    expires: COOKIE_EXPIRES,
    secure: true,
    sameSite: 'strict'
  });
  // Backup in localStorage
  localStorage.setItem(TOKEN_KEY, token);
}

// Store user info in both cookie and localStorage
export function setAuthUser(user: StoredUser): void {
  const userStr = JSON.stringify(user);
  // Set in cookie with expiration
  Cookies.set(USER_KEY, userStr, {
    expires: COOKIE_EXPIRES,
    secure: true,
    sameSite: 'strict'
  });
  // Backup in localStorage
  localStorage.setItem(USER_KEY, userStr);
}

// Get token from cookie or fallback to localStorage
export function getAuthToken(): string | null {
  return Cookies.get(TOKEN_KEY) || localStorage.getItem(TOKEN_KEY);
}

// Get user from cookie or fallback to localStorage
export function getAuthUser(): StoredUser | null {
  const userStr = Cookies.get(USER_KEY) || localStorage.getItem(USER_KEY);
  if (!userStr) return null;
  
  try {
    return JSON.parse(userStr);
  } catch (error) {
    console.warn('Error parsing stored user:', error);
    return null;
  }
}

// Remove auth data from both cookie and localStorage
export function removeAuthData(): void {
  // Remove from cookies
  Cookies.remove(TOKEN_KEY);
  Cookies.remove(USER_KEY);
  // Remove from localStorage
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

// Add auth header to API requests
export function getAuthHeaders(): HeadersInit {
  const token = getAuthToken();
  return {
    'Authorization': token ? `Token ${token}` : '',
    'Content-Type': 'application/json'
  };
}