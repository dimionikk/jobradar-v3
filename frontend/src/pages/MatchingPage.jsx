import { useState, useEffect } from "react";
import { getMatchingVacancies, generateCoverLetter } from "../api/ai";

function ScoreBar({ score }) {
  const color = score >= 60 ? "bg-signal" : score >= 30 ? "bg-alert" : "bg-text-dim";
  return (
    <div className="flex items-center gap-2 shrink-0">
      <div className="w-16 h-1.5 bg-surface-raised rounded-full overflow-hidden">
        <div className={`h-full ${color}`} style={{ width: `${score}%` }} />
      </div>
      <span className="font-mono text-sm text-text w-9 text-right">{score}%</span>
    </div>
  );
}

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
    return (
      <div className="max-w-3xl mx-auto px-6 py-8">
        <p className="text-text-dim text-sm font-mono">
          <span className="text-signal">●</span> AI аналізує вакансії...
        </p>
      </div>
    );
  }

  if (loadError) {
    return <p className="text-danger p-6">{loadError}</p>;
  }

  return (
    <div className="max-w-3xl mx-auto px-6 py-8">
      <h1 className="text-xl font-semibold mb-6">AI-підбір вакансій</h1>

      {actionError && (
        <p className="text-sm text-danger border-l-2 border-danger pl-3 mb-4">
          {actionError}
        </p>
      )}

      {matches.length === 0 && (
        <p className="text-text-dim text-sm">
          Немає відповідних вакансій. Заповни профіль для точнішого підбору.
        </p>
      )}

      <div className="flex flex-col gap-2">
        {matches.map((m) => (
          <div
            key={m.vacancy_id}
            className="bg-surface border border-line rounded-lg p-4 hover:border-signal-dim transition-colors"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="min-w-0">
                <h2 className="font-medium text-text truncate">{m.title}</h2>
                <p className="text-sm text-text-dim">{m.company || "Компанія не вказана"}</p>
              </div>
              <ScoreBar score={m.match_score} />
            </div>

            <p className="text-sm text-text-dim mt-3">{m.reason}</p>

            <div className="mt-3 pt-3 border-t border-line">
              <button
                onClick={() => handleGenerate(m.vacancy_id)}
                disabled={generatingId === m.vacancy_id || !!letters[m.vacancy_id]}
                className="text-sm text-signal hover:text-signal-dim disabled:text-text-dim transition-colors"
              >
                {generatingId === m.vacancy_id
                  ? "Генерую..."
                  : letters[m.vacancy_id]
                  ? "Лист згенеровано"
                  : "Згенерувати супровідний лист"}
              </button>
              {letters[m.vacancy_id] && (
                <p className="text-sm text-text mt-2 whitespace-pre-wrap bg-surface-raised p-3 rounded">
                  {letters[m.vacancy_id]}
                </p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MatchingPage;