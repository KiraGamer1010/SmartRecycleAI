import { Activity, Cpu, Database, Network } from "lucide-react";
import StatusBadge from "../common/StatusBadge.jsx";

export default function Header() {
  return (
    <header className="border-b border-white/10 bg-graphite/82 backdrop-blur">
      <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-4 sm:px-6 lg:flex-row lg:items-center lg:justify-between lg:px-8">
        <div>
          <p className="text-sm text-emerald-100/60">Centro operativo</p>
          <h2 className="text-xl font-semibold text-white">SmartRecycleAI</h2>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <StatusBadge variant="online">
            <Activity size={14} aria-hidden="true" />
            API lista
          </StatusBadge>
          <StatusBadge variant="neutral">
            <Cpu size={14} aria-hidden="true" />
            IA modular
          </StatusBadge>
          <StatusBadge variant="neutral">
            <Database size={14} aria-hidden="true" />
            PostgreSQL
          </StatusBadge>
          <StatusBadge variant="neutral">
            <Network size={14} aria-hidden="true" />
            Docker ready
          </StatusBadge>
        </div>
      </div>
    </header>
  );
}
