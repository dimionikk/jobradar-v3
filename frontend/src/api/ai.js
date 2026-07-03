import { apiRequest } from "./client";

export function generateCoverLetter(vacancyId) {
  return apiRequest("/ai/cover-letter", {
    method: "POST",
    body: JSON.stringify({ vacancy_id: vacancyId }),
  });
}

export function getMatchingVacancies() {
  return apiRequest("/ai/matching");
}
