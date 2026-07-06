import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { ROUTES } from "../routes";

const NAV_LINKS = [
  { to: ROUTES.VACANCIES, label: "Вакансії" },
  { to: ROUTES.SAVED_VACANCIES, label: "Збережені" },
  { to: ROUTES.APPLICATIONS, label: "Заявки" },
  { to: ROUTES.MATCHING, label: "AI-підбір" },
  { to: ROUTES.PROFILE, label: "Профіль" },
];

function Navbar() {
  const { logout } = useAuth();
  const location = useLocation();

  return (
    <nav className="border-b border-line bg-surface">
      <div className="max-w-4xl mx-auto flex items-center gap-6 px-6 py-4">
        <div className="flex items-center gap-2 pr-2">
          <span className="w-2 h-2 rounded-full bg-signal animate-pulse" />
          <span className="font-mono font-semibold tracking-tight text-text">
            jobradar
          </span>
        </div>

        <div className="flex items-center gap-1">
          {NAV_LINKS.map((link) => {
            const isActive = location.pathname === link.to;
            return (
              <Link
                key={link.to}
                to={link.to}
                className={`px-3 py-1.5 rounded text-sm transition-colors ${
                  isActive
                    ? "bg-surface-raised text-signal"
                    : "text-text-dim hover:text-text"
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </div>

        <button
          onClick={logout}
          className="ml-auto text-sm text-text-dim hover:text-danger transition-colors"
        >
          Вийти
        </button>
      </div>
    </nav>
  );
}

export default Navbar;