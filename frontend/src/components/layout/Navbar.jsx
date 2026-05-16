import { Activity, Database, Recycle } from "lucide-react";
import { Link, NavLink } from "react-router-dom";
import Badge from "../ui/Badge.jsx";
import Button from "../ui/Button.jsx";
import { navigationItems } from "./navigationItems.js";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-30 border-b border-white/10 bg-graphite/88 backdrop-blur-xl">
      <div className="mx-auto flex h-[var(--nav-height)] max-w-[var(--layout-max-width)] items-center justify-between gap-4 px-4 sm:px-6 lg:px-8">
        <Link className="focus-ring flex items-center gap-3 rounded-lg" to="/">
          <span className="rounded-lg border border-mint/25 bg-mint/10 p-2 text-mint shadow-glow">
            <Recycle aria-hidden="true" size={22} />
          </span>
          <div>
            <p className="text-sm font-semibold text-white">SmartRecycleAI</p>
            <p className="text-xs text-emerald-100/55">AI recycling platform</p>
          </div>
        </Link>

        <nav className="hidden items-center gap-1 lg:flex" aria-label="Navegacion principal">
          {navigationItems.map(({ to, label, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                [
                  "focus-ring rounded-lg px-3 py-2 text-sm font-medium transition",
                  isActive
                    ? "bg-white/10 text-white"
                    : "text-emerald-50/68 hover:bg-white/[0.08] hover:text-white"
                ].join(" ")
              }
            >
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="hidden items-center gap-2 md:flex">
          <Badge variant="mint">
            <Activity size={14} aria-hidden="true" />
            API lista
          </Badge>
          <Badge variant="neutral">
            <Database size={14} aria-hidden="true" />
            PostgreSQL
          </Badge>
        </div>

        <Button
          as={Link}
          to="/theory"
          className="hidden sm:inline-flex"
          variant="secondary"
        >
          Ver teoría
        </Button>
      </div>
    </header>
  );
}
