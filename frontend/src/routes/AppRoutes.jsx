import { Route, Routes } from "react-router-dom";
import MainLayout from "../layouts/MainLayout.jsx";
import DashboardPage from "../pages/DashboardPage.jsx";
import HomePage from "../pages/HomePage.jsx";
import NotFoundPage from "../pages/NotFoundPage.jsx";
import OperationsPage from "../pages/OperationsPage.jsx";
import RecognitionPage from "../pages/RecognitionPage.jsx";
import TheoryPage from "../pages/TheoryPage.jsx";

export default function AppRoutes() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route index element={<HomePage />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="recognition" element={<RecognitionPage />} />
        <Route path="operations" element={<OperationsPage />} />
        <Route path="theory" element={<TheoryPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}
