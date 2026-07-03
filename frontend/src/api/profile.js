import { apiRequest } from "./client";

export function getProfile() {
  return apiRequest("/profile/");
}
