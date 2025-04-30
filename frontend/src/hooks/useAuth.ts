// src/hooks/useAuth.ts
import { useState, useEffect } from 'react';
import { login, signup, me } from '../services/auth';
import { useNavigate } from 'react-router-dom';
import { UserType } from '../types';

export default function useAuth() {
  const [user, setUser] = useState<UserType>({} as UserType);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const history = useNavigate();
  // Verificar se o usuário está logado
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      getLoggedUser();
    }
  }, []);

  // Função para login
  const handleLogin = async (username: string, password: string) => {
    setLoading(true);
    try {
      const response = await login({ username, password });
      localStorage.setItem('token', response.access);
      const data = await me();
      setUser({ ...data });
      localStorage.setItem('user', JSON.stringify(data));
      history('/feed');
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  // Função para signup
  const handleSignup = async (username: string, email: string, password: string) => {
    setLoading(true);
    try {
      const response = await signup({ username, email, password });
      localStorage.setItem('token', response.token);
      history('login');
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Signup failed');
    } finally {
      setLoading(false);
    }
  };

  const getLoggedUser = () => {
    const storedUser = localStorage.getItem('user');
    let userData = {} as UserType;
    if (storedUser && !user.id) {
      const data = JSON.parse(storedUser);
      userData = { ...data } as UserType;
      setUser({ ...data });
    }
    return userData;
  }

  return {
    user,
    loading,
    error,
    getLoggedUser,
    handleLogin,
    handleSignup,
  };
}
