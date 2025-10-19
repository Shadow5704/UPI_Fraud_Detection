import api from "./api";

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  profile?: {
    phone_number: string;
    upi_id: string;
  };
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  password: string;
  password2: string;
  phone_number?: string;
  upi_id?: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
  user: User;
}

export const authService = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await api.post("/api/auth/login/", credentials);
    const { access, refresh } = response.data;

    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);

    return response.data;
  },

  async register(data: RegisterData): Promise<AuthResponse> {
    const response = await api.post("/api/auth/register/", data);
    const { access, refresh } = response.data;

    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);

    return response.data;
  },

  async logout(): Promise<void> {
    const refresh_token = localStorage.getItem("refresh_token");
    if (refresh_token) {
      try {
        await api.post("/api/auth/logout/", { refresh_token });
      } catch (error) {
        console.error("Logout error:", error);
      }
    }
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  },

  async getProfile(): Promise<User> {
    const response = await api.get("/api/auth/profile/");
    return response.data;
  },

  async updateProfile(data: Partial<User>): Promise<User> {
    const response = await api.patch("/api/auth/profile/", data);
    return response.data;
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem("access_token");
  },
};
