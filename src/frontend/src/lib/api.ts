import axios from "axios";
const baseURL = import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_LOCAL_DOMAIN;

export const api = axios.create({
  baseURL: baseURL
});

api.interceptors.request.use((config) => {
  const token =
    localStorage.getItem("access_token") ||
    import.meta.env.VITE_DEV_TOKEN;

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});