import { useState, useEffect } from "react";
import { getVacancies } from "../api/vacancies";
import { saveVacancy, getSavedVacancies } from "../api/savedVacancies";
import { createApplication, getApplications } from "../api/applications";

const SOURCES = ["djinni", "dou", "remotive", "workua"];
const PAGE_SIZE = 20;

function VacanciesPage() {
  const [vacancies, setVacancies] = useState([]);
  const [loadError, setLoadError] = useState("");
  const [actionError, setActionError] = useState("");
  const [savedIds, setSavedIds] = useState(new Set());
  const [appliedIds, setAppliedIds] = useState(new Set());
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);

  const [searchInput, setSearchInput] = useState("");
  const [search, setSearch] = useState("");
  const [city, setCity] = useState("");
  const [source, setSource] = useState("");

  useEffect(() => {
    const timer = setTimeout(() => {
      setSearch(searchInput);
      setPage(1);
    }, 400);
    return () => clearTimeout(timer);
  }, [searchInput]);

  useEffect(() => {
    Promise.all([getSavedVacancies(), getApplications()])
      .then(([saved, applications]) => {
        setSavedIds(new Set(saved.map((v) => v.id)));
        setAppliedIds(new Set(applications.map((a) => a.vacancy.id)));
      })
      .catch((err) => setLoadError(err.message));
  }, []);

  useEffect(() => {
    setLoading(true);
    getVacancies({ search, city, source, page })
      .then(setVacancies)
      .catch((err) => setLoadError(err.message))
      .finally(() => setLoading(false));
  }, [search, city, source, page]);

  function handleCityChange(value) {
    setCity(value);
    setPage(1);
  }

  function handleSourceChange(value) {
    setSource(value);
    setPage(1);
  }

  async function handleSave(id) {
    setActionError("");
    try {
      await saveVacancy(id);
      setSavedIds((prev) => new Set(prev).add(id));
    } catch (err) {
      setActionError(err.message);
    }
  }

  async function handleApply(id) {
    setActionError("");
    try {
      await createApplication(id);
      setAppliedIds((prev) => new Set(prev).add(id));
    } catch (err) {
      setActionError(err.message);
    }
  }

  if (loadError) {
    return <p className="text-red-600 p-6">{loadError}</p>;
  }

  return (
    <div className="max-w-2xl mx-auto mt-10 p-6">
      <h1 className="text-2xl font-bold mb-4">Вакансії</h1>

      <div className="flex flex-col gap-2 mb-6">
        <input
          type="text"
          placeholder="Пошук за назвою чи описом"
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          className="border p-2 rounded"
        />
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Місто"
            value={city}
            onChange={(e) => handleCityChange(e.target.value)}
            className="border p-2 rounded flex-1"
          />
          <select
            value={source}
            onChange={(e) => handleSourceChange(e.target.value)}
            className="border p-2 rounded"
          >
            <option value="">Усі джерела</option>
            {SOURCES.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>
      </div>

      {actionError && <p className="text-red-600 mb-4">{actionError}</p>}

      {loading ? (
        <p>Завантаження...</p>
      ) : vacancies.length === 0 ? (
        <p>Нічого не знайдено.</p>
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
          disabled={vacancies.length < PAGE_SIZE || loading}
          className="text-sm text-blue-600 disabled:text-gray-400"
        >
          Далі →
        </button>
      </div>
    </div>
  );
}

export default VacanciesPage;