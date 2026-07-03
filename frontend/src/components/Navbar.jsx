import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Navbar() {
  const { logout } = useAuth();

  return (
    <nav className="flex gap-4 p-4 border-b items-center">
      <Link to="/vacancies" className="text-blue-600 underline">Вакансії</Link>
      <Link to="/saved-vacancies" className="text-blue-600 underline">Збережені</Link>
      <Link to="/applications" className="text-blue-600 underline">Заявки</Link>
      <Link to="/profile" className="text-blue-600 underline">Профіль</Link>
      <button onClick={logout} className="ml-auto text-red-600">Вийти</button>
    </nav>
  );
}

export default Navbar;