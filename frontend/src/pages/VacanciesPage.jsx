import { useState, useEffect } from "react";
import { getSavedVacancies, removeSavedVacancy } from "../api/savedVacancies";

function SavedVacanciesPage() {
  const [vacancies, setVacancies] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    getSavedVacancies()
      .then(setVacancies)
      .catch((err) => setError(err.message));
  }, []);

  async function handleRemove(id) {
    try {
      await removeSavedVacancy(id);
      setVacancies((prev) => prev.filter((v) => v.id !== id));
    } catch (err) {
      setError(err.message);
    }
  }

  if (error) {
    return <p className="text-red-600 p-6">{error}</p>;
  }

  return (
    <div className="max-w-2xl mx-auto mt-10 p-6">
      <h1 className="text-2xl font-bold mb-4">Збережені вакансії</h1>
      {vacancies.length === 0 && <p>Нема збережених вакансій.</p>}
      <div className="flex flex-col gap-3">
        {vacancies.map((v) => (
          <div key={v.id} className="border p-4 rounded">
            <h2 className="font-semibold">{v.title}</h2>
            <p className="text-sm">{v.company || "Компанія не вказана"}</p>
            <div className="flex gap-3 mt-2">
              <a href={v.url} target="_blank" className="text-blue-600 underline text-sm">
                Переглянути
              </a>
              <button onClick={() => handleRemove(v.id)} className="text-sm text-red-600">
                Прибрати
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SavedVacanciesPage;