import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { 
  setAuthToken, 
  setAuthUser, 
  removeAuthData, 
  getAuthToken, 
  getAuthUser 
} from '@/utils/auth';
import * as authApi from '@/apis/auth';
import type { User } from '@/types';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  token: string | null;
}

// Initialize state from stored auth data
const storedToken = getAuthToken();
const storedUser = getAuthUser();

const initialState: AuthState = {
  user: storedUser,
  isAuthenticated: !!storedToken && !!storedUser,
  isLoading: false,
  error: null,
  token: storedToken
};

export const signIn = createAsyncThunk(
  'auth/signIn',
  async ({ email, password }: { email: string; password: string }) => {
    const response = await authApi.signIn(email, password);
    // Store auth token
    setAuthToken(response.token);
    // Create a mock user for now since the API doesn't return user data
    const mockUser: User = {
      id: '1',
      name: email.split('@')[0], // Use email username as name
      email,
      avatarUrl: `https://ui-avatars.com/api/?name=${encodeURIComponent(email.split('@')[0])}&background=random`
    };
    setAuthUser(mockUser);
    return { token: response.token, user: mockUser };
  }
);

export const signUp = createAsyncThunk(
  'auth/signUp',
  async ({ name, email, password }: { name: string; email: string; password: string }) => {
    const response = await authApi.signUp(name, email, password);
    // Store auth token
    setAuthToken(response.token);
    // Create a mock user for now since the API doesn't return user data
    const mockUser: User = {
      id: '1',
      name,
      email,
      avatarUrl: `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=random`
    };
    setAuthUser(mockUser);
    return { token: response.token, user: mockUser };
  }
);

export const signOut = createAsyncThunk(
  'auth/signOut',
  async () => {
    removeAuthData();
    return true;
  }
);

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      // Sign In
      .addCase(signIn.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(signIn.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isAuthenticated = true;
        state.user = action.payload.user;
        state.token = action.payload.token;
      })
      .addCase(signIn.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to sign in';
      })
      // Sign Up
      .addCase(signUp.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(signUp.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isAuthenticated = true;
        state.user = action.payload.user;
        state.token = action.payload.token;
      })
      .addCase(signUp.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to sign up';
      })
      // Sign Out
      .addCase(signOut.fulfilled, (state) => {
        state.user = null;
        state.isAuthenticated = false;
        state.token = null;
      });
  }
});

export default authSlice.reducer;