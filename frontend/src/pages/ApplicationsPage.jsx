import { useState, useEffect } from "react";
import { getApplications, updateApplication, deleteApplication } from "../api/applications";

const STATUSES = ["applied", "interview", "offer", "rejected", "withdrawn"];

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
    return <p className="text-red-600 p-6">{loadError}</p>;
  }

  return (
    <div className="max-w-2xl mx-auto mt-10 p-6">
      <h1 className="text-2xl font-bold mb-4">Мої заявки</h1>

      {actionError && <p className="text-red-600 mb-4">{actionError}</p>}

      {loading ? (
        <p>Завантаження...</p>
      ) : applications.length === 0 ? (
        <p>Заявок ще нема.</p>
      ) : (
        <div className="flex flex-col gap-3">
          {applications.map((a) => (
            <div key={a.id} className="border p-4 rounded">
              <h2 className="font-semibold">{a.vacancy.title}</h2>
              <p className="text-sm">{a.vacancy.company || "Компанія не вказана"}</p>
              <div className="flex gap-3 mt-2 items-center">
                <select
                  value={a.status}
                  onChange={(e) => handleStatusChange(a.id, e.target.value)}
                  disabled={processingId === a.id}
                  className="border p-1 rounded text-sm disabled:bg-gray-100"
                >
                  {STATUSES.map((s) => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
                <button
                  onClick={() => handleDelete(a.id)}
                  disabled={processingId === a.id}
                  className="text-sm text-red-600 disabled:text-gray-400"
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