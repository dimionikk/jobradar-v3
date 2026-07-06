import { useState, useEffect } from "react";
import { getProfile, updateProfile } from "../api/profile";
import { useAuth } from "../context/AuthContext";

function Field({ label, children }) {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-xs text-text-dim uppercase tracking-wide">{label}</label>
      {children}
    </div>
  );
}

const inputClass =
  "bg-surface-raised border border-line rounded px-3 py-2 text-text placeholder:text-text-dim focus:outline-none focus:ring-1 focus:ring-signal focus:border-signal transition-colors";

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
      <div className="max-w-md mx-auto mt-20 px-6">
        <p className="text-danger mb-4">{loadError}</p>
        <button
          onClick={logout}
          className="bg-danger text-ink font-medium rounded px-4 py-2.5 w-full"
        >
          Вийти
        </button>
      </div>
    );
  }

  if (!profile) {
    return <p className="text-text-dim text-sm p-8 text-center">Завантаження...</p>;
  }

  return (
    <div className="max-w-md mx-auto px-6 py-8">
      <h1 className="text-xl font-semibold">Профіль</h1>
      <p className="text-sm text-text-dim font-mono mb-6">{profile.email}</p>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <Field label="Стек технологій">
          <input
            type="text"
            value={form.stack}
            onChange={(e) => handleChange("stack", e.target.value)}
            className={inputClass}
          />
        </Field>

        <div className="grid grid-cols-2 gap-3">
          <Field label="Років досвіду">
            <input
              type="number"
              value={form.experience_years}
              onChange={(e) => handleChange("experience_years", e.target.value)}
              className={`${inputClass} font-mono`}
            />
          </Field>
          <Field label="ЗП, $">
            <input
              type="number"
              value={form.salary_expectation}
              onChange={(e) => handleChange("salary_expectation", e.target.value)}
              className={`${inputClass} font-mono`}
            />
          </Field>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <Field label="Місто">
            <input
              type="text"
              value={form.city}
              onChange={(e) => handleChange("city", e.target.value)}
              className={inputClass}
            />
          </Field>
          <Field label="Формат роботи">
            <input
              type="text"
              placeholder="remote/office"
              value={form.work_type}
              onChange={(e) => handleChange("work_type", e.target.value)}
              className={inputClass}
            />
          </Field>
        </div>

        <Field label="Про себе">
          <textarea
            value={form.bio}
            onChange={(e) => handleChange("bio", e.target.value)}
            className={inputClass}
            rows={3}
          />
        </Field>

        <Field label="Текст резюме">
          <textarea
            value={form.resume_text}
            onChange={(e) => handleChange("resume_text", e.target.value)}
            className={inputClass}
            rows={4}
          />
        </Field>

        {saveError && (
          <p className="text-sm text-danger border-l-2 border-danger pl-3">{saveError}</p>
        )}

        <button
          type="submit"
          disabled={saving}
          className="bg-signal text-ink font-medium rounded px-4 py-2.5 hover:bg-signal-dim disabled:bg-surface-raised disabled:text-text-dim transition-colors"
        >
          {saving ? "Зберігаю..." : "Зберегти"}
        </button>
      </form>

      <button
        onClick={logout}
        className="mt-3 w-full text-sm text-text-dim hover:text-danger transition-colors py-2"
      >
        Вийти
      </button>
    </div>
  );
}

export default ProfilePage;