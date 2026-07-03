import { useState, useEffect } from "react";
import { getProfile } from "../api/profile";
import { useAuth } from "../context/AuthContext";

function ProfilePage() {
  const { logout } = useAuth();
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getProfile()
      .then(setProfile)
      .catch((err) => setError(err.message));
  }, []);

  if (error) {
    return (
      <div className="max-w-sm mx-auto mt-20 p-6 border rounded">
        <p className="text-red-600">{error}</p>
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
    <div className="max-w-sm mx-auto mt-20 p-6 border rounded">
      <h1 className="text-2xl font-bold mb-4">Профіль</h1>
      <p><span className="font-semibold">Email:</span> {profile.email}</p>
      <p><span className="font-semibold">Стек:</span> {profile.stack || "не вказано"}</p>
      <p><span className="font-semibold">Досвід:</span> {profile.experience_years ?? "не вказано"} років</p>
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