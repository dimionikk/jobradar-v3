import { apiRequest } from "./client";

const SAVED_VACANCIES_PATH = "/saved-vacancies";

export function getSavedVacancies() {
  return apiRequest(`${SAVED_VACANCIES_PATH}/`);
}

export function saveVacancy(vacancyId) {
  return apiRequest(`${SAVED_VACANCIES_PATH}/${vacancyId}`, { method: "POST" });
}

export function removeSavedVacancy(vacancyId) {
  return apiRequest(`${SAVED_VACANCIES_PATH}/${vacancyId}`, { method: "DELETE" });
}