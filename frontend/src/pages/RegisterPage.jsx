import { useState } from "react";
import { Link, Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { ROUTES } from "../routes";

function RegisterPage() {
  const { register, isAuthenticated } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await register(email, password);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  if (isAuthenticated) {
    return <Navigate to={ROUTES.VACANCIES} />;
  }

  return (
    <div className="min-h-[calc(100vh-73px)] flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <div className="mb-6 text-center">
          <span className="font-mono text-sm text-signal tracking-widest uppercase">
            Реєстрація
          </span>
        </div>

        <form
          onSubmit={handleSubmit}
          className="bg-surface border border-line rounded-lg p-6 flex flex-col gap-4"
        >
          <div className="flex flex-col gap-1.5">
            <label className="text-xs text-text-dim uppercase tracking-wide">
              Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="bg-surface-raised border border-line rounded px-3 py-2 text-text focus:outline-none focus:ring-1 focus:ring-signal focus:border-signal transition-colors"
              required
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs text-text-dim uppercase tracking-wide">
              Пароль
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="bg-surface-raised border border-line rounded px-3 py-2 text-text focus:outline-none focus:ring-1 focus:ring-signal focus:border-signal transition-colors"
              required
            />
            <span className="text-xs text-text-dim">Мінімум 8 символів</span>
          </div>

          {error && (
            <p className="text-sm text-danger border-l-2 border-danger pl-3">
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="mt-2 bg-signal text-ink font-medium rounded px-4 py-2.5 hover:bg-signal-dim disabled:bg-surface-raised disabled:text-text-dim transition-colors"
          >
            {loading ? "Реєструємо..." : "Зареєструватись"}
          </button>
        </form>

        <p className="mt-5 text-center text-sm text-text-dim">
          Вже є акаунт?{" "}
          <Link to={ROUTES.LOGIN} className="text-signal hover:text-signal-dim">
            Увійти
          </Link>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;