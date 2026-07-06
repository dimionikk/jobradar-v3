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
    return <p className="text-red-600 p-6">{loadError}</p>;
  }

  return (
    <div className="max-w-2xl mx-auto mt-10 p-6">
      <h1 className="text-2xl font-bold mb-4">Збережені вакансії</h1>

      {actionError && <p className="text-red-600 mb-4">{actionError}</p>}

      {loading ? (
        <p>Завантаження...</p>
      ) : vacancies.length === 0 ? (
        <p>Нема збережених вакансій.</p>
      ) : (
        <div className="flex flex-col gap-3">
          {vacancies.map((v) => (
            <div key={v.id} className="border p-4 rounded">
              <h2 className="font-semibold">{v.title}</h2>
              <p className="text-sm">{v.company || "Компанія не вказана"}</p>
              <div className="flex gap-3 mt-2">
                <a href={v.url} target="_blank" className="text-blue-600 underline text-sm">
                  Переглянути
                </a>
                <button
                  onClick={() => handleRemove(v.id)}
                  disabled={removingId === v.id}
                  className="text-sm text-red-600 disabled:text-gray-400"
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