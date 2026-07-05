import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { LOGIN_PATH } from "../api/constants";

function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) {
    return <Navigate to={LOGIN_PATH} />;
  }
  return children;
}

export default ProtectedRoute;