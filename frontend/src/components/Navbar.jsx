import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { ROUTES } from "../routes";

const NAV_LINKS = [
  { to: ROUTES.VACANCIES, label: "Вакансії" },
  { to: ROUTES.SAVED_VACANCIES, label: "Збережені" },
  { to: ROUTES.APPLICATIONS, label: "Заявки" },
  { to: ROUTES.PROFILE, label: "Профіль" },
  { to: ROUTES.MATCHING, label: "AI-підбір" },
];

function Navbar() {
  const { logout } = useAuth();

  return (
    <nav className="flex gap-4 p-4 border-b items-center">
      {NAV_LINKS.map((link) => (
        <Link key={link.to} to={link.to} className="text-blue-600 underline">
          {link.label}
        </Link>
      ))}
      <button onClick={logout} className="ml-auto text-red-600">Вийти</button>
    </nav>
  );
}

export default Navbar;