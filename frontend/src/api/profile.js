import { apiRequest } from "./client";

export function getProfile() {
  return apiRequest("/profile/");
}

export function updateProfile(data) {
  return apiRequest("/profile/", {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}