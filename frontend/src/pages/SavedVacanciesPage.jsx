import { useState, useEffect } from "react";
import { getSavedVacancies, removeSavedVacancy } from "../api/savedVacancies";

function SavedVacanciesPage() {
  const [vacancies, setVacancies] = useState([]);
  const [loadError, setLoadError] = useState("");
  const [actionError, setActionError] = useState("");
  const [loading, setLoading] = useState(true);
  const [removingId, setRemovingId] = useState(null);

  useEffect(() => {
    getSavedVacancies()
      .then(setVacancies)
      .catch((err) => setLoadError(err.message))
      .finally(() => setLoading(false));
  }, []);

  async function handleRemove(id) {
    setActionError("");
    setRemovingId(id);
    try {
      await removeSavedVacancy(id);
      setVacancies((prev) => prev.filter((v) => v.id !== id));
    } catch (err) {
      setActionError(err.message);
    } finally {
      setRemovingId(null);
    }
  }

  if (loadError) {
    return <p className="text-danger p-6">{loadError}</p>;
  }

  return (
    <div className="max-w-3xl mx-auto px-6 py-8">
      <h1 className="text-xl font-semibold mb-6">Збережені вакансії</h1>

      {actionError && (
        <p className="text-sm text-danger border-l-2 border-danger pl-3 mb-4">
          {actionError}
        </p>
      )}

      {loading ? (
        <p className="text-text-dim text-sm">Завантаження...</p>
      ) : vacancies.length === 0 ? (
        <p className="text-text-dim text-sm">Нема збережених вакансій.</p>
      ) : (
        <div className="flex flex-col gap-2">
          {vacancies.map((v) => (
            <div
              key={v.id}
              className="bg-surface border border-line rounded-lg p-4 hover:border-signal-dim transition-colors"
            >
              <h2 className="font-medium text-text">{v.title}</h2>
              <p className="text-sm text-text-dim">{v.company || "Компанія не вказана"}</p>

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
                  onClick={() => handleRemove(v.id)}
                  disabled={removingId === v.id}
                  className="text-danger hover:opacity-80 disabled:text-text-dim transition-colors"
                >
                  {removingId === v.id ? "Видаляю..." : "Прибрати"}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default SavedVacanciesPage;