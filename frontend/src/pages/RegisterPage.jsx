import { useState } from "react";
import { Link, Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function RegisterPage() {
  const { register, isAuthenticated } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      await register(email, password);
    } catch (err) {
      setError(err.message);
    }
  }

if (isAuthenticated) {
  return <Navigate to="/profile" />;
}

  return (
    <div className="max-w-sm mx-auto mt-20 p-6 border rounded">
      <h1 className="text-2xl font-bold mb-4">Реєстрація</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="border p-2 rounded"
        />
        <input
          type="password"
          placeholder="Пароль (мінімум 8 символів)"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="border p-2 rounded"
        />
        {error && <p className="text-red-600">{error}</p>}
        <button type="submit" className="bg-blue-600 text-white p-2 rounded">
          Зареєструватись
        </button>
      </form>
      <p className="mt-4 text-sm">
        Вже є акаунт?{" "}
        <Link to="/login" className="text-blue-600 underline">
          Увійти
        </Link>
      </p>
    </div>
  );
}

export default RegisterPage;