import { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '@/hooks';
import { fetchDocuments } from '@/store/documentsSlice';

export function useDocuments() {
  const dispatch = useAppDispatch();
  const { documents, isLoading, error } = useAppSelector(state => state.documents);

  useEffect(() => {
    dispatch(fetchDocuments());
  }, [dispatch]);

  return { documents, isLoading, error };
}