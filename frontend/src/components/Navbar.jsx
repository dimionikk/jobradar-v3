import { Link, useLocation } from "react-router-dom";
import { Briefcase, Bookmark, FileText, Sparkles, User, LogOut } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { ROUTES } from "../routes";

const NAV_LINKS = [
  { to: ROUTES.VACANCIES, label: "Вакансії", icon: Briefcase },
  { to: ROUTES.SAVED_VACANCIES, label: "Збережені", icon: Bookmark },
  { to: ROUTES.APPLICATIONS, label: "Заявки", icon: FileText },
  { to: ROUTES.MATCHING, label: "AI-підбір", icon: Sparkles },
  { to: ROUTES.PROFILE, label: "Профіль", icon: User },
];

function Navbar() {
  const { logout } = useAuth();
  const location = useLocation();

  return (
    <>
      <nav className="hidden sm:block border-b border-line bg-surface">
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

      <nav className="sm:hidden flex items-center justify-between px-4 py-3 border-b border-line bg-surface">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-signal animate-pulse" />
          <span className="font-mono font-semibold text-text text-sm">jobradar</span>
        </div>
        <button onClick={logout} className="text-text-dim">
          <LogOut className="w-5 h-5" />
        </button>
      </nav>

      <nav className="sm:hidden fixed bottom-0 left-0 right-0 flex items-center justify-around bg-surface border-t border-line py-2 z-10">
        {NAV_LINKS.map((link) => {
          const isActive = location.pathname === link.to;
          const Icon = link.icon;
          return (
            <Link
              key={link.to}
              to={link.to}
              className={`flex flex-col items-center gap-0.5 px-2 py-1 text-[10px] ${
                isActive ? "text-signal" : "text-text-dim"
              }`}
            >
              <Icon className="w-5 h-5" />
              {link.label}
            </Link>
          );
        })}
      </nav>
    </>
  );
}

export default Navbar;