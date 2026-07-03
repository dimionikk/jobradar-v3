import { useState, useEffect } from "react";
import { getApplications, updateApplication, deleteApplication } from "../api/applications";

const STATUSES = ["applied", "interview", "offer", "rejected", "withdrawn"];

function ApplicationsPage() {
  const [applications, setApplications] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    getApplications()
      .then(setApplications)
      .catch((err) => setError(err.message));
  }, []);

  async function handleStatusChange(id, status) {
    try {
      const updated = await updateApplication(id, { status });
      setApplications((prev) => prev.map((a) => (a.id === id ? updated : a)));
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleDelete(id) {
    try {
      await deleteApplication(id);
      setApplications((prev) => prev.filter((a) => a.id !== id));
    } catch (err) {
      setError(err.message);
    }
  }

  if (error) {
    return <p className="text-red-600 p-6">{error}</p>;
  }

  return (
    <div className="max-w-2xl mx-auto mt-10 p-6">
      <h1 className="text-2xl font-bold mb-4">Мої заявки</h1>
      {applications.length === 0 && <p>Заявок ще нема.</p>}
      <div className="flex flex-col gap-3">
        {applications.map((a) => (
          <div key={a.id} className="border p-4 rounded">
            <h2 className="font-semibold">{a.vacancy.title}</h2>
            <p className="text-sm">{a.vacancy.company || "Компанія не вказана"}</p>
            <div className="flex gap-3 mt-2 items-center">
              <select
                value={a.status}
                onChange={(e) => handleStatusChange(a.id, e.target.value)}
                className="border p-1 rounded text-sm"
              >
                {STATUSES.map((s) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
              <button onClick={() => handleDelete(a.id)} className="text-sm text-red-600">
                Видалити
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ApplicationsPage;
