import { create } from "zustand";
import { UserProfile } from "@/types";
import { getToken, clearSession, getMe } from "@/lib/auth";

interface AuthState {
  token: string | null;
  user: UserProfile | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  setUser: (user: UserProfile) => void;
  setToken: (token: string) => void;
  logout: () => void;
  hydrate: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: null,
  user: null,
  isAuthenticated: false,
  isLoading: true,

  setUser: (user) => set({ user, isAuthenticated: true }),

  setToken: (token) => set({ token }),

  logout: () => {
    clearSession();
    set({ token: null, user: null, isAuthenticated: false });
    window.location.href = "/login";
  },

  hydrate: async () => {
    const token = getToken();
    if (!token) {
      set({ isLoading: false });
      return;
    }
    try {
      const user = await getMe() as UserProfile;
      set({ token, user, isAuthenticated: true, isLoading: false });
    } catch {
      clearSession();
      set({ token: null, user: null, isAuthenticated: false, isLoading: false });
    }
  },
}));