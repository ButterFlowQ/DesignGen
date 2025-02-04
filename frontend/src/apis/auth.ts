import { apiRequest } from './config';
import { generateDummyToken } from '@/utils/auth';
import type { User } from '@/types';

interface AuthResponse {
  user: User;
  token: string;
}

export async function signIn(email: string, password: string): Promise<AuthResponse> {
  // TODO: Replace with actual API call
  await new Promise(resolve => setTimeout(resolve, 500));

  if (email === 'test@example.com' && password === 'password') {
    const mockUser: User = {
      id: '1',
      name: 'John Doe',
      email,
      avatarUrl: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?fit=facearea&facepad=2&w=256&h=256&q=80'
    };
    return {
      user: mockUser,
      token: generateDummyToken(mockUser.id)
    };
  }

  throw new Error('Invalid credentials');
}

export async function signUp(
  name: string, 
  email: string, 
  password: string
): Promise<AuthResponse> {
  // TODO: Replace with actual API call
  await new Promise(resolve => setTimeout(resolve, 500));

  const mockUser: User = {
    id: '1',
    name,
    email,
    avatarUrl: `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=random`
  };
  return {
    user: mockUser,
    token: generateDummyToken(mockUser.id)
  };
}