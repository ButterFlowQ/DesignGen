import { configureStore } from '@reduxjs/toolkit';
import chatReducer from './chatSlice';
import authReducer from './authSlice';
import documentsReducer from './documentsSlice';

export const store = configureStore({
  reducer: {
    chat: chatReducer,
    auth: authReducer,
    documents: documentsReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export const getState = store.getState;
export const dispatch = store.dispatch;