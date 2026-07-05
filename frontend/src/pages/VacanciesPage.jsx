import { useState, useEffect } from "react";
import { getVacancies } from "../api/vacancies";
import { saveVacancy, getSavedVacancies } from "../api/savedVacancies";
import { createApplication, getApplications } from "../api/applications";

function VacanciesPage() {
  const [vacancies, setVacancies] = useState([]);
  const [error, setError] = useState("");
  const [savedIds, setSavedIds] = useState(new Set());
  const [appliedIds, setAppliedIds] = useState(new Set());
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getSavedVacancies(), getApplications()])
      .then(([saved, applications]) => {
        setSavedIds(new Set(saved.map((v) => v.id)));
        setAppliedIds(new Set(applications.map((a) => a.vacancy.id)));
      })
      .catch((err) => setError(err.message));
  }, []);

  useEffect(() => {
    setLoading(true);
    getVacancies({ page })
      .then(setVacancies)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [page]);

  async function handleSave(id) {
    try {
      await saveVacancy(id);
      setSavedIds((prev) => new Set(prev).add(id));
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleApply(id) {
    try {
      await createApplication(id);
      setAppliedIds((prev) => new Set(prev).add(id));
    } catch (err) {
      setError(err.message);
    }
  }

  if (error) {
    return <p className="text-red-600 p-6">{error}</p>;
  }

  return (
    <div className="max-w-2xl mx-auto mt-10 p-6">
      <h1 className="text-2xl font-bold mb-4">Вакансії</h1>

      {loading ? (
        <p>Завантаження...</p>
      ) : (
        <div className="flex flex-col gap-3">
          {vacancies.map((v) => (
            <div key={v.id} className="border p-4 rounded">
              <h2 className="font-semibold">{v.title}</h2>
              <p className="text-sm">{v.company || "Компанія не вказана"}</p>
              <p className="text-sm text-gray-600">{v.city || "Місто не вказано"} · {v.salary || "ЗП не вказана"}</p>
              <div className="flex gap-3 mt-2">
                <a href={v.url} target="_blank" className="text-blue-600 underline text-sm">
                  Переглянути
                </a>
                <button
                  onClick={() => handleSave(v.id)}
                  disabled={savedIds.has(v.id)}
                  className="text-sm text-green-600 disabled:text-gray-400"
                >
                  {savedIds.has(v.id) ? "Збережено" : "Зберегти"}
                </button>
                <button
                  onClick={() => handleApply(v.id)}
                  disabled={appliedIds.has(v.id)}
                  className="text-sm text-purple-600 disabled:text-gray-400"
                >
                  {appliedIds.has(v.id) ? "Подано" : "Подати заявку"}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="flex justify-between items-center mt-6">
        <button
          onClick={() => setPage((p) => Math.max(1, p - 1))}
          disabled={page === 1 || loading}
          className="text-sm text-blue-600 disabled:text-gray-400"
        >
          ← Назад
        </button>
        <span className="text-sm text-gray-600">Сторінка {page}</span>
        <button
          onClick={() => setPage((p) => p + 1)}
          disabled={vacancies.length < 20 || loading}
          className="text-sm text-blue-600 disabled:text-gray-400"
        >
          Далі →
        </button>
      </div>
    </div>
  );
}

export default VacanciesPage;