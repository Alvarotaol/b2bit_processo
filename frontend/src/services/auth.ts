// src/services/auth.ts
import Api from "./http";

interface LoginData {
  username: string;
  password: string;
}

interface SignupData {
  username: string;
  email: string;
  password: string;
}

export async function login(data: LoginData) {
  const response = await Api.post('/users/login/', data, false);
  return response.data;
}

export async function signup(data: SignupData) {
  const response = await Api.post('/users/signup/', data, false);
  return response.data;
}

export const handleLogout = async () => {
  try {
    await logout();
    localStorage.removeItem('token');
    return true;
  } catch (err) {
    console.error('Logout failed', err);
    return false;
  }
};


async function logout() {
  const response = await Api.post('/users/logout/');
  return response.data;
}

export async function me() {
  const response = await Api.get('/users/me/');
  return response.data;
}