import { createContext, useContext, useState } from "react";
import { loginUser, registerUser, logoutUser } from "../api/auth";
import { TOKEN_KEY } from "../api/constants";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem(TOKEN_KEY));

  async function login(email, password) {
    const result = await loginUser(email, password);
    localStorage.setItem(TOKEN_KEY, result.access_token);
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
      localStorage.removeItem(TOKEN_KEY);
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