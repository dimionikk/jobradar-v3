import { apiRequest } from "./client";

export function getVacancies({ search, city, source, workType, page = 1 } = {}) {
  const params = new URLSearchParams();
  if (search) params.set("search", search);
  if (city) params.set("city", city);
  if (source) params.set("source", source);
  if (workType) params.set("work_type", workType);
  params.set("page", page);
  return apiRequest(`/vacancies/?${params.toString()}`);
}