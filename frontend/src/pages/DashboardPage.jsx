import { motion } from "framer-motion";
import {
  ArrowUpRight,
  Boxes,
  Gauge,
  Leaf,
  Recycle
} from "lucide-react";
import MetricCard from "../components/common/MetricCard.jsx";
import SectionHeader from "../components/common/SectionHeader.jsx";
import StatusBadge from "../components/common/StatusBadge.jsx";

const streams = [
  { name: "PET transparente", score: "97.4%", status: "Reciclable" },
  { name: "Aluminio", score: "94.1%", status: "Alta pureza" },
  { name: "Carton mixto", score: "88.6%", status: "Revision" }
];

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <SectionHeader
        eyebrow="SmartRecycleAI"
        title="Control inteligente de reciclaje"
        action={
          <button className="inline-flex items-center justify-center gap-2 rounded-lg bg-mint px-4 py-2 text-sm font-semibold text-graphite transition hover:bg-emerald-300">
            <ArrowUpRight aria-hidden="true" size={18} />
            Nuevo analisis
          </button>
        }
      />

      <section className="grid gap-4 md:grid-cols-3">
        <MetricCard icon={Recycle} label="Material procesado" value="12.8 t" />
        <MetricCard
          icon={Gauge}
          label="Precision estimada"
          value="96.2%"
          tone="signal"
        />
        <MetricCard
          icon={Leaf}
          label="Desvio evitado"
          value="8.4 t"
          tone="solar"
        />
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.35fr_0.65fr]">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="overflow-hidden rounded-lg border border-white/10 bg-panel/86"
        >
          <div className="flex items-center justify-between border-b border-white/10 px-5 py-4">
            <div>
              <h2 className="text-lg font-semibold text-white">
                Flujo de clasificacion
              </h2>
              <p className="text-sm text-emerald-100/58">
                Vision artificial separada del backend operativo.
              </p>
            </div>
            <StatusBadge variant="online">Activo</StatusBadge>
          </div>
          <div className="relative h-72 overflow-hidden scanner-surface">
            <div className="absolute left-0 right-0 top-8 h-1 bg-mint/80 shadow-glow scan-line" />
            <div className="absolute inset-x-6 bottom-6 grid gap-3 sm:grid-cols-3">
              {streams.map((stream) => (
                <div
                  key={stream.name}
                  className="rounded-lg border border-white/12 bg-graphite/72 p-4 backdrop-blur"
                >
                  <p className="text-sm font-semibold text-white">
                    {stream.name}
                  </p>
                  <p className="mt-3 text-2xl font-semibold text-mint">
                    {stream.score}
                  </p>
                  <p className="mt-1 text-xs text-emerald-100/60">
                    {stream.status}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.08 }}
          className="rounded-lg border border-white/10 bg-panel/86 p-5"
        >
          <div className="flex items-center gap-3">
            <span className="rounded-lg border border-signal/25 bg-signal/10 p-3 text-signal">
              <Boxes aria-hidden="true" size={22} />
            </span>
            <div>
              <h2 className="text-lg font-semibold text-white">
                Modulos desacoplados
              </h2>
              <p className="text-sm text-emerald-100/58">
                Frontend, API, IA y datos escalan por separado.
              </p>
            </div>
          </div>
          <div className="mt-6 space-y-3">
            {["React + Vite", "FastAPI + SQLAlchemy", "YOLO + OpenCV"].map(
              (item) => (
                <div
                  key={item}
                  className="flex items-center justify-between rounded-lg border border-white/10 bg-white/[0.04] px-4 py-3"
                >
                  <span className="text-sm text-emerald-50/82">{item}</span>
                  <StatusBadge variant="neutral">Ready</StatusBadge>
                </div>
              )
            )}
          </div>
        </motion.div>
      </section>
    </div>
  );
}
