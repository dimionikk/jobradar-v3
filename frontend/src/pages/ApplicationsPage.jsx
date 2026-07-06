import { useState, useEffect } from "react";
import { getApplications, updateApplication, deleteApplication } from "../api/applications";

const STATUSES = ["applied", "interview", "offer", "rejected", "withdrawn"];

const STATUS_COLORS = {
  applied: "bg-text-dim",
  interview: "bg-alert",
  offer: "bg-signal",
  rejected: "bg-danger",
  withdrawn: "bg-text-dim",
};

function ApplicationsPage() {
  const [applications, setApplications] = useState([]);
  const [loadError, setLoadError] = useState("");
  const [actionError, setActionError] = useState("");
  const [loading, setLoading] = useState(true);
  const [processingId, setProcessingId] = useState(null);

  useEffect(() => {
    getApplications()
      .then(setApplications)
      .catch((err) => setLoadError(err.message))
      .finally(() => setLoading(false));
  }, []);

  async function handleStatusChange(id, status) {
    setActionError("");
    setProcessingId(id);
    try {
      const updated = await updateApplication(id, { status });
      setApplications((prev) => prev.map((a) => (a.id === id ? updated : a)));
    } catch (err) {
      setActionError(err.message);
    } finally {
      setProcessingId(null);
    }
  }

  async function handleDelete(id) {
    setActionError("");
    setProcessingId(id);
    try {
      await deleteApplication(id);
      setApplications((prev) => prev.filter((a) => a.id !== id));
    } catch (err) {
      setActionError(err.message);
    } finally {
      setProcessingId(null);
    }
  }

  if (loadError) {
    return <p className="text-danger p-6">{loadError}</p>;
  }

  return (
    <div className="max-w-3xl mx-auto px-6 py-8">
      <h1 className="text-xl font-semibold mb-6">Мої заявки</h1>

      {actionError && (
        <p className="text-sm text-danger border-l-2 border-danger pl-3 mb-4">
          {actionError}
        </p>
      )}

      {loading ? (
        <p className="text-text-dim text-sm">Завантаження...</p>
      ) : applications.length === 0 ? (
        <p className="text-text-dim text-sm">Заявок ще нема.</p>
      ) : (
        <div className="flex flex-col gap-2">
          {applications.map((a) => (
            <div
              key={a.id}
              className="bg-surface border border-line rounded-lg p-4 hover:border-signal-dim transition-colors"
            >
              <div className="flex items-center gap-2">
                <span className={`w-1.5 h-1.5 rounded-full ${STATUS_COLORS[a.status]}`} />
                <h2 className="font-medium text-text">{a.vacancy.title}</h2>
              </div>
              <p className="text-sm text-text-dim mt-1">{a.vacancy.company || "Компанія не вказана"}</p>

              <div className="flex gap-3 mt-3 pt-3 border-t border-line items-center">
                <select
                  value={a.status}
                  onChange={(e) => handleStatusChange(a.id, e.target.value)}
                  disabled={processingId === a.id}
                  className="bg-surface-raised border border-line rounded px-2 py-1 text-sm text-text focus:outline-none focus:ring-1 focus:ring-signal disabled:opacity-50 transition-colors"
                >
                  {STATUSES.map((s) => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
                <button
                  onClick={() => handleDelete(a.id)}
                  disabled={processingId === a.id}
                  className="text-sm text-danger hover:opacity-80 disabled:text-text-dim transition-colors"
                >
                  {processingId === a.id ? "..." : "Видалити"}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ApplicationsPage;