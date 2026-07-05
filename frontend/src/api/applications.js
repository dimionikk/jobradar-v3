import { apiRequest } from "./client";

const APPLICATIONS_PATH = "/applications";

export function getApplications() {
  return apiRequest(`${APPLICATIONS_PATH}/`);
}

export function createApplication(vacancyId) {
  return apiRequest(`${APPLICATIONS_PATH}/${vacancyId}`, { method: "POST" });
}

export function updateApplication(applicationId, data) {
  return apiRequest(`${APPLICATIONS_PATH}/${applicationId}`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

export function deleteApplication(applicationId) {
  return apiRequest(`${APPLICATIONS_PATH}/${applicationId}`, { method: "DELETE" });
}