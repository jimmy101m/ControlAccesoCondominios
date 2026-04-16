import { api } from "./api";

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}

export function clearSession(): void {
  localStorage.removeItem("token");
}

export async function login(email: string, password: string) {
  const data = await api.post<{ token: string }>("/auth/login", {
    email,
    password,
  });
  localStorage.setItem("token", data.token);
  return data;
}

export async function getMe() {
  return api.post("/auth/me", {});
}

export async function logout() {
  try {
    await api.post("/auth/logout", {});
  } finally {
    clearSession();
    window.location.href = "/login";
  }
}