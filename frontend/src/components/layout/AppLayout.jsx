import { Camera, Factory, LayoutDashboard, Recycle } from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";
import Header from "./Header.jsx";

const navItems = [
  { to: "/", label: "Panel", icon: LayoutDashboard },
  { to: "/recognition", label: "Vision IA", icon: Camera },
  { to: "/operations", label: "Operaciones", icon: Factory }
];

export default function AppLayout() {
  return (
    <div className="min-h-screen">
      <Header />
      <div className="mx-auto grid max-w-7xl gap-6 px-4 py-6 sm:px-6 lg:grid-cols-[240px_minmax(0,1fr)] lg:px-8">
        <aside className="rounded-lg border border-white/10 bg-panel/82 p-3 shadow-glow lg:sticky lg:top-6 lg:h-[calc(100vh-8rem)]">
          <div className="mb-4 hidden items-center gap-3 px-2 py-2 lg:flex">
            <span className="rounded-lg border border-mint/25 bg-mint/10 p-2 text-mint">
              <Recycle aria-hidden="true" size={22} />
            </span>
            <div>
              <p className="text-sm font-semibold text-white">SRAI Core</p>
              <p className="text-xs text-emerald-100/55">Arquitectura limpia</p>
            </div>
          </div>
          <nav className="flex gap-2 overflow-x-auto lg:flex-col lg:overflow-visible">
            {navItems.map(({ to, label, icon: Icon }) => (
              <NavLink
                key={to}
                to={to}
                end={to === "/"}
                className={({ isActive }) =>
                  [
                    "inline-flex min-w-fit items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium transition",
                    isActive
                      ? "bg-mint text-graphite"
                      : "text-emerald-50/72 hover:bg-white/[0.08] hover:text-white"
                  ].join(" ")
                }
              >
                <Icon aria-hidden="true" size={18} />
                {label}
              </NavLink>
            ))}
          </nav>
        </aside>
        <main className="min-w-0">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
