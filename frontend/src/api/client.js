import { TOKEN_KEY, REFRESH_TOKEN_KEY } from "./constants";
import { ROUTES } from "../routes";

const API_URL = "https://89-167-93-204.nip.io";

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function getRefreshToken() {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
}

export function setTokens(accessToken, refreshToken) {
  localStorage.setItem(TOKEN_KEY, accessToken);
  localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
}

export function clearTokens() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
}

function redirectToLogin() {
  clearTokens();
  window.location.href = ROUTES.LOGIN;
}

let refreshPromise = null;

async function tryRefreshToken() {
  const refreshToken = getRefreshToken();
  if (!refreshToken) {
    return false;
  }

  if (!refreshPromise) {
    refreshPromise = fetch(`${API_URL}/auth/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: refreshToken }),
    })
      .then((res) => (res.ok ? res.json() : null))
      .finally(() => {
        refreshPromise = null;
      });
  }

  const result = await refreshPromise;
  if (!result) {
    return false;
  }

  setTokens(result.access_token, result.refresh_token);
  return true;
}

export async function apiRequest(endpoint, options = {}) {
  const { skipAuthRefresh, ...fetchOptions } = options;
  const token = getToken();
  const headers = {
    "Content-Type": "application/json",
    ...fetchOptions.headers,
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...fetchOptions,
    headers,
  });

  if (response.status === 401 && token && !skipAuthRefresh) {
    const refreshed = await tryRefreshToken();
    if (refreshed) {
      return apiRequest(endpoint, { ...options, skipAuthRefresh: true });
    }
    redirectToLogin();
    return new Promise(() => {});
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.detail || "Щось пішло не так");
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}