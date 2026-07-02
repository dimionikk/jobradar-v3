const API_URL = "https://89-167-93-204.nip.io";

function getToken() {
  return localStorage.getItem("access_token");
}

export async function apiRequest(endpoint, options = {}) {
  const token = getToken();

  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.detail || "Щось пішло не так");
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}
