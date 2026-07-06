import { useState, useEffect } from "react";
import { getMatchingVacancies, generateCoverLetter } from "../api/ai";

function MatchingPage() {
  const [matches, setMatches] = useState([]);
  const [loadError, setLoadError] = useState("");
  const [actionError, setActionError] = useState("");
  const [loading, setLoading] = useState(true);
  const [letters, setLetters] = useState({});
  const [generatingId, setGeneratingId] = useState(null);

  useEffect(() => {
    getMatchingVacancies()
      .then((result) => setMatches(result.matches))
      .catch((err) => setLoadError(err.message))
      .finally(() => setLoading(false));
  }, []);

  async function handleGenerate(vacancyId) {
    setActionError("");
    setGeneratingId(vacancyId);
    try {
      const result = await generateCoverLetter(vacancyId);
      setLetters((prev) => ({ ...prev, [vacancyId]: result.cover_letter }));
    } catch (err) {
      setActionError(err.message);
    } finally {
      setGeneratingId(null);
    }
  }

  if (loading) {
    return <p className="p-6">AI аналізує вакансії, зачекай...</p>;
  }

  if (loadError) {
    return <p className="text-red-600 p-6">{loadError}</p>;
  }

  return (
    <div className="max-w-2xl mx-auto mt-10 p-6">
      <h1 className="text-2xl font-bold mb-4">AI-підбір вакансій</h1>

      {actionError && <p className="text-red-600 mb-4">{actionError}</p>}

      {matches.length === 0 && <p>Немає відповідних вакансій. Заповни профіль для точнішого підбору.</p>}
      <div className="flex flex-col gap-3">
        {matches.map((m) => (
          <div key={m.vacancy_id} className="border p-4 rounded">
            <div className="flex justify-between items-start">
              <h2 className="font-semibold">{m.title}</h2>
              <span className="text-sm font-bold text-blue-600">{m.match_score}%</span>
            </div>
            <p className="text-sm">{m.company || "Компанія не вказана"}</p>
            <p className="text-sm text-gray-600 mt-1">{m.reason}</p>
            <button
              onClick={() => handleGenerate(m.vacancy_id)}
              disabled={generatingId === m.vacancy_id || !!letters[m.vacancy_id]}
              className="text-sm text-purple-600 mt-2 disabled:text-gray-400"
            >
              {generatingId === m.vacancy_id
                ? "Генерую..."
                : letters[m.vacancy_id]
                ? "Лист згенеровано"
                : "Згенерувати супровідний лист"}
            </button>
            {letters[m.vacancy_id] && (
              <p className="text-sm mt-2 whitespace-pre-wrap bg-gray-50 p-2 rounded">
                {letters[m.vacancy_id]}
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default MatchingPage;