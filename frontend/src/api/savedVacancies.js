import { apiRequest } from "./client";

export function getSavedVacancies() {
  return apiRequest("/saved-vacancies/");
}

export function saveVacancy(vacancyId) {
  return apiRequest(`/saved-vacancies/${vacancyId}`, { method: "POST" });
}

export function removeSavedVacancy(vacancyId) {
  return apiRequest(`/saved-vacancies/${vacancyId}`, { method: "DELETE" });
}
