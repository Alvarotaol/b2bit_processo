// src/hooks/useAuth.ts
import { useState, useEffect } from 'react';
import { login, signup, logout, me } from '../services/auth';
import { useNavigate } from 'react-router-dom';
import { UserType } from '../types';

export default function useAuth() {
  const [user, setUser] = useState<UserType | null>(null);
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
      setUser({ ...response });
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
      getLoggedUser();
      history('login');
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Signup failed');
    } finally {
      setLoading(false);
    }
  };

  // Função para logout
  const handleLogout = async () => {
    try {
      await logout();
      localStorage.removeItem('token');
      setUser(null);
      history('/login');
    } catch (err) {
      console.error('Logout failed', err);
    }
  };

  const getLoggedUser = async () => {
    const token = localStorage.getItem('token');
    if(user == null) return
    if (token) {
      const response = await me();
      localStorage.setItem('token', response.access);
      setUser({ ...response });
    }
  }

  return {
    user,
    loading,
    error,
    handleLogin,
    handleSignup,
    handleLogout,
  };
}
