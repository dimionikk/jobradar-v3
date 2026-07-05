import { apiRequest } from "./client";

export function getVacancies({ search, city, source, workType, page = 1 } = {}) {
  const filters = { search, city, source, work_type: workType };

  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(filters)) {
    if (value) params.set(key, value);
  }
  params.set("page", page);

  return apiRequest(`/vacancies/?${params.toString()}`);
}