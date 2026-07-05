const API_URL = "https://89-167-93-204.nip.io";
const TOKEN_KEY = "access_token";
const LOGIN_PATH = "/login";

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export async function apiRequest(endpoint, options = {}) {
  const token = getToken();

  const headers = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401 && token) {
    localStorage.removeItem(TOKEN_KEY);
    window.location.href = LOGIN_PATH;
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