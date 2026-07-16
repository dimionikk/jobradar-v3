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
  const [cityInput, setCityInput] = useState("");
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
    const timer = setTimeout(() => {
      setCity(cityInput);
      setPage(1);
    }, 400);
    return () => clearTimeout(timer);
  }, [cityInput]);

  useEffect(() => {
    Promise.all([getSavedVacancies(), getApplications()])
      .then(([saved, applications]) => {
        setSavedIds(new Set(saved.map((v) => v.id)));
        setAppliedIds(new Set(applications.map((a) => a.vacancy.id)));
      })
      .catch((err) => setLoadError(err.message));
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    getVacancies({ search, city, source, page }, { signal: controller.signal })
      .then(setVacancies)
      .catch((err) => {
        if (err.name === "AbortError") return;
        setLoadError(err.message);
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [search, city, source, page]);

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
    return <p className="text-danger p-6">{loadError}</p>;
  }

  return (
    <div className="max-w-3xl mx-auto px-6 py-8">
      <h1 className="text-xl font-semibold mb-6">Вакансії</h1>
      <div className="flex flex-col sm:flex-row gap-2 mb-6">
        <input
          type="text"
          placeholder="Пошук за назвою чи описом"
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          className="flex-1 bg-surface border border-line rounded px-3 py-2 text-sm text-text placeholder:text-text-dim focus:outline-none focus:ring-1 focus:ring-signal focus:border-signal transition-colors"
        />
        <input
          type="text"
          placeholder="Місто"
          value={cityInput}
          onChange={(e) => setCityInput(e.target.value)}
          className="sm:w-40 bg-surface border border-line rounded px-3 py-2 text-sm text-text placeholder:text-text-dim focus:outline-none focus:ring-1 focus:ring-signal focus:border-signal transition-colors"
        />
        <select
          value={source}
          onChange={(e) => handleSourceChange(e.target.value)}
          className="sm:w-40 bg-surface border border-line rounded px-3 py-2 text-sm text-text focus:outline-none focus:ring-1 focus:ring-signal focus:border-signal transition-colors"
        >
          <option value="">Усі джерела</option>
          {SOURCES.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </div>
      {actionError && (
        <p className="text-sm text-danger border-l-2 border-danger pl-3 mb-4">
          {actionError}
        </p>
      )}
      {loading ? (
        <p className="text-text-dim text-sm">Скануємо джерела...</p>
      ) : vacancies.length === 0 ? (
        <p className="text-text-dim text-sm">Нічого не знайдено.</p>
      ) : (
        <div className="flex flex-col gap-2">
          {vacancies.map((v) => (
            <div
              key={v.id}
              className="bg-surface border border-line rounded-lg p-4 hover:border-signal-dim transition-colors"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="min-w-0">
                  <h2 className="font-medium text-text truncate">{v.title}</h2>
                  <p className="text-sm text-text-dim">{v.company || "Компанія не вказана"}</p>
                </div>
                <span className="shrink-0 text-xs font-mono text-text-dim uppercase border border-line rounded px-1.5 py-0.5">
                  {v.source}
                </span>
              </div>
              <div className="flex items-center gap-3 mt-3 text-sm">
                <span className="text-text-dim">{v.city || "Місто не вказано"}</span>
                <span className="font-mono text-signal">{v.salary || "ЗП не вказана"}</span>
              </div>
              <div className="flex gap-4 mt-3 pt-3 border-t border-line text-sm">
                <a
                  href={v.url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-text-dim hover:text-text transition-colors"
                >
                  Переглянути
                </a>
                <button
                  onClick={() => handleSave(v.id)}
                  disabled={savedIds.has(v.id)}
                  className="text-signal hover:text-signal-dim disabled:text-text-dim transition-colors"
                >
                  {savedIds.has(v.id) ? "Збережено" : "Зберегти"}
                </button>
                <button
                  onClick={() => handleApply(v.id)}
                  disabled={appliedIds.has(v.id)}
                  className="text-alert hover:opacity-80 disabled:text-text-dim transition-colors"
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
          className="text-sm text-text-dim hover:text-text disabled:opacity-40 transition-colors"
        >
          ← Назад
        </button>
        <span className="text-sm font-mono text-text-dim">{String(page).padStart(2, "0")}</span>
        <button
          onClick={() => setPage((p) => p + 1)}
          disabled={vacancies.length < PAGE_SIZE || loading}
          className="text-sm text-text-dim hover:text-text disabled:opacity-40 transition-colors"
        >
          Далі →
        </button>
      </div>
    </div>
  );
}

export default VacanciesPage;