import { Boxes, Cpu, Database, GitBranch } from "lucide-react";
import MiniTrendChart from "../charts/MiniTrendChart.jsx";
import Badge from "../ui/Badge.jsx";
import GlassCard from "../ui/GlassCard.jsx";

const modules = [
  { icon: Boxes, name: "Frontend", detail: "React, Vite, TailwindCSS" },
  { icon: Database, name: "Backend", detail: "FastAPI, SQLAlchemy, PostgreSQL" },
  { icon: Cpu, name: "AI Engine", detail: "OpenCV, Ultralytics YOLO, Pandas" },
  { icon: GitBranch, name: "MLOps", detail: "Docker, CI/CD, trazabilidad" }
];

export default function SystemOverview() {
  return (
    <section className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
      <GlassCard>
        <div className="flex items-center justify-between gap-4">
          <div>
            <h2 className="text-lg font-semibold text-white">Arquitectura modular</h2>
            <p className="mt-1 text-sm text-emerald-100/58">
              Separacion profesional entre experiencia visual, API, datos e IA.
            </p>
          </div>
          <Badge variant="signal">Clean stack</Badge>
        </div>
        <div className="mt-5 grid gap-3">
          {modules.map(({ icon: Icon, name, detail }) => (
            <div
              key={name}
              className="flex items-center gap-3 rounded-lg border border-white/10 bg-white/[0.045] p-3"
            >
              <span className="rounded-lg border border-mint/20 bg-mint/10 p-2 text-mint">
                <Icon size={18} aria-hidden="true" />
              </span>
              <div>
                <p className="text-sm font-semibold text-white">{name}</p>
                <p className="text-xs text-emerald-100/55">{detail}</p>
              </div>
            </div>
          ))}
        </div>
      </GlassCard>

      <GlassCard>
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-white">Eficiencia proyectada</h2>
            <p className="mt-1 text-sm text-emerald-100/58">
              Visualizacion inicial para comportamiento operacional.
            </p>
          </div>
          <Badge variant="mint">+18%</Badge>
        </div>
        <div className="mt-5">
          <MiniTrendChart />
        </div>
      </GlassCard>
    </section>
  );
}
