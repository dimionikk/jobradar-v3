import { apiRequest } from "./client";

export function getApplications() {
  return apiRequest("/applications/");
}

export function createApplication(vacancyId) {
  return apiRequest(`/applications/${vacancyId}`, { method: "POST" });
}

export function updateApplication(applicationId, data) {
  return apiRequest(`/applications/${applicationId}`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

export function deleteApplication(applicationId) {
  return apiRequest(`/applications/${applicationId}`, { method: "DELETE" });
}
