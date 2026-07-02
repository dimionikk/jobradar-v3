import { createContext, useContext, useState } from "react";
import { loginUser, registerUser, logoutUser } from "../api/auth";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("access_token"));

  async function login(email, password) {
    const result = await loginUser(email, password);
    localStorage.setItem("access_token", result.access_token);
    setToken(result.access_token);
  }

  async function register(email, password) {
    await registerUser(email, password);
  }

  async function logout() {
    try {
      await logoutUser();
    } finally {
      localStorage.removeItem("access_token");
      setToken(null);
    }
  }

  const value = {
    token,
    isAuthenticated: !!token,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}

