import { NavLink } from "react-router-dom";
import Badge from "../ui/Badge.jsx";
import { navigationItems } from "./navigationItems.js";

export default function Sidebar() {
  return (
    <aside className="glass-panel p-3 lg:sticky lg:top-24 lg:h-[calc(100vh-7.5rem)]">
      <div className="mb-4 hidden px-2 py-2 lg:block">
        <Badge variant="signal">Enterprise UI</Badge>
        <p className="mt-3 text-sm font-semibold text-white">Centro operativo</p>
        <p className="mt-1 text-xs leading-5 text-emerald-100/54">
          Navegación modular para operaciones, IA y documentación académica.
        </p>
      </div>

      <nav className="flex gap-2 overflow-x-auto lg:flex-col lg:overflow-visible" aria-label="Menu lateral">
        {navigationItems.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              [
                "focus-ring inline-flex min-w-fit items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium transition",
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
  );
}
