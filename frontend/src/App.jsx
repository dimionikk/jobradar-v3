import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ProfilePage from "./pages/ProfilePage";
import VacanciesPage from "./pages/VacanciesPage";
import SavedVacanciesPage from "./pages/SavedVacanciesPage";
import ProtectedRoute from "./components/ProtectedRoute";
import Navbar from "./components/Navbar";
import ApplicationsPage from "./pages/ApplicationsPage";
import MatchingPage from "./pages/MatchingPage";
import { ROUTES } from "./routes";

function Layout({ children }) {
  return (
    <>
      <Navbar />
      <div className="pb-20 sm:pb-0">{children}</div>
    </>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path={ROUTES.LOGIN} element={<LoginPage />} />
        <Route path={ROUTES.REGISTER} element={<RegisterPage />} />
        <Route
          path={ROUTES.PROFILE}
          element={
            <ProtectedRoute>
              <Layout><ProfilePage /></Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path={ROUTES.VACANCIES}
          element={
            <ProtectedRoute>
              <Layout><VacanciesPage /></Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path={ROUTES.SAVED_VACANCIES}
          element={
            <ProtectedRoute>
              <Layout><SavedVacanciesPage /></Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path={ROUTES.APPLICATIONS}
          element={
            <ProtectedRoute>
              <Layout><ApplicationsPage /></Layout>
            </ProtectedRoute>
          }
        />
        <Route
          path={ROUTES.MATCHING}
          element={
            <ProtectedRoute>
              <Layout><MatchingPage /></Layout>
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to={ROUTES.LOGIN} />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;