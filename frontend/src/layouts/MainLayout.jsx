import { Outlet } from "react-router-dom";
import Navbar from "../components/layout/Navbar.jsx";
import Sidebar from "../components/layout/Sidebar.jsx";

export default function MainLayout() {
  return (
    <div className="min-h-screen">
      <Navbar />
      <div className="mx-auto grid max-w-[var(--layout-max-width)] gap-6 px-4 py-6 sm:px-6 lg:grid-cols-[244px_minmax(0,1fr)] lg:px-8">
        <Sidebar />
        <main className="min-w-0 pb-10">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
