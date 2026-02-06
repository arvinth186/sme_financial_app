// src/api/auth.ts
import api from "./axios";

export const loginApi = async (email: string, password: string) => {
  const res = await api.post("/auth/login", { email, password });
  return res.data; // { access_token }
};

export const registerApi = async (email: string, password: string) => {
  const res = await api.post("/auth/register", { email, password });
  return res.data;
};
