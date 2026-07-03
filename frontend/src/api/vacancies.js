import { apiRequest } from "./client";

export function getVacancies({ city, source, page = 1 } = {}) {
  const params = new URLSearchParams();
  if (city) params.set("city", city);
  if (source) params.set("source", source);
  params.set("page", page);
  return apiRequest(`/vacancies/?${params.toString()}`);
}
