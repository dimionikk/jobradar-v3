import { useState, useEffect } from "react";
import { getProfile, updateProfile } from "../api/profile";
import { useAuth } from "../context/AuthContext";

function ProfilePage() {
  const { logout } = useAuth();
  const [profile, setProfile] = useState(null);
  const [loadError, setLoadError] = useState("");
  const [saveError, setSaveError] = useState("");
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({
    stack: "",
    experience_years: "",
    salary_expectation: "",
    city: "",
    work_type: "",
    bio: "",
    resume_text: "",
  });

  useEffect(() => {
    getProfile()
      .then((data) => {
        setProfile(data);
        setForm({
          stack: data.stack || "",
          experience_years: data.experience_years ?? "",
          salary_expectation: data.salary_expectation ?? "",
          city: data.city || "",
          work_type: data.work_type || "",
          bio: data.bio || "",
          resume_text: data.resume_text || "",
        });
      })
      .catch((err) => setLoadError(err.message));
  }, []);

  function handleChange(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSaveError("");
    setSaving(true);
    try {
      const payload = {
        ...form,
        experience_years: form.experience_years === "" ? null : Number(form.experience_years),
        salary_expectation: form.salary_expectation === "" ? null : Number(form.salary_expectation),
      };
      const updated = await updateProfile(payload);
      setProfile(updated);
    } catch (err) {
      setSaveError(err.message);
    } finally {
      setSaving(false);
    }
  }

  if (loadError) {
    return (
      <div className="max-w-sm mx-auto mt-20 p-6 border rounded">
        <p className="text-red-600 mb-4">{loadError}</p>
        <button
          onClick={logout}
          className="bg-red-600 text-white p-2 rounded w-full"
        >
          Вийти
        </button>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="max-w-sm mx-auto mt-20 p-6 border rounded">
        <p>Завантаження...</p>
      </div>
    );
  }

  return (
    <div className="max-w-sm mx-auto mt-10 p-6 border rounded">
      <h1 className="text-2xl font-bold mb-4">Профіль</h1>
      <p className="text-sm text-gray-600 mb-4">{profile.email}</p>
      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <input
          type="text"
          placeholder="Стек технологій"
          value={form.stack}
          onChange={(e) => handleChange("stack", e.target.value)}
          className="border p-2 rounded"
        />
        <input
          type="number"
          placeholder="Років досвіду"
          value={form.experience_years}
          onChange={(e) => handleChange("experience_years", e.target.value)}
          className="border p-2 rounded"
        />
        <input
          type="number"
          placeholder="Бажана зарплата ($)"
          value={form.salary_expectation}
          onChange={(e) => handleChange("salary_expectation", e.target.value)}
          className="border p-2 rounded"
        />
        <input
          type="text"
          placeholder="Місто"
          value={form.city}
          onChange={(e) => handleChange("city", e.target.value)}
          className="border p-2 rounded"
        />
        <input
          type="text"
          placeholder="Формат роботи (remote/office/hybrid)"
          value={form.work_type}
          onChange={(e) => handleChange("work_type", e.target.value)}
          className="border p-2 rounded"
        />
        <textarea
          placeholder="Про себе"
          value={form.bio}
          onChange={(e) => handleChange("bio", e.target.value)}
          className="border p-2 rounded"
          rows={3}
        />
        <textarea
          placeholder="Текст резюме"
          value={form.resume_text}
          onChange={(e) => handleChange("resume_text", e.target.value)}
          className="border p-2 rounded"
          rows={4}
        />
        {saveError && <p className="text-red-600">{saveError}</p>}
        <button
          type="submit"
          disabled={saving}
          className="bg-blue-600 text-white p-2 rounded disabled:bg-gray-400"
        >
          {saving ? "Зберігаю..." : "Зберегти"}
        </button>
      </form>
      <button
        onClick={logout}
        className="mt-4 bg-red-600 text-white p-2 rounded w-full"
      >
        Вийти
      </button>
    </div>
  );
}

export default ProfilePage;