import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ProfilePage from "./pages/ProfilePage";
import VacanciesPage from "./pages/VacanciesPage";
import SavedVacanciesPage from "./pages/SavedVacanciesPage";
import ProtectedRoute from "./components/ProtectedRoute";
import Navbar from "./components/Navbar";

function Layout({ children }) {
  return (
    <>
      <Navbar />
      {children}
    </>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <Layout><ProfilePage /></Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/vacancies"
          element={
            <ProtectedRoute>
              <Layout><VacanciesPage /></Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/saved-vacancies"
          element={
            <ProtectedRoute>
              <Layout><SavedVacanciesPage /></Layout>
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;