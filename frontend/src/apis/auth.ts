import { apiRequest } from './config';

interface AuthResponse {
  token: string;
}

export async function signIn(email: string, password: string): Promise<AuthResponse> {
  return await apiRequest('/authenticate/login', {
    method: 'POST',
    body: JSON.stringify({ email, password })
  });
}

export async function signUp(
  username: string,
  email: string, 
  password: string
): Promise<AuthResponse> {
  return await apiRequest('/authenticate/signup', {
    method: 'POST',
    body: JSON.stringify({ username, email, password })
  });
}