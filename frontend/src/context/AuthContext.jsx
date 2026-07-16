import { createContext, useContext, useState } from "react";
import { loginUser, registerUser, logoutUser } from "../api/auth";
import { setTokens, clearTokens } from "../api/client";
import { TOKEN_KEY } from "../api/constants";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem(TOKEN_KEY));

  async function login(email, password) {
    const result = await loginUser(email, password);
    setTokens(result.access_token, result.refresh_token);
    setToken(result.access_token);
  }

  async function register(email, password) {
    await registerUser(email, password);
    await login(email, password);
  }

  async function logout() {
    try {
      await logoutUser();
    } finally {
      clearTokens();
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