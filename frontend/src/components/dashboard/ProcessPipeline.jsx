import { motion } from "framer-motion";
import { CheckCircle2 } from "lucide-react";
import Badge from "../ui/Badge.jsx";
import GlassCard from "../ui/GlassCard.jsx";

const streams = [
  { name: "PET transparente", score: "97.4%", status: "Reciclable" },
  { name: "Aluminio", score: "94.1%", status: "Alta pureza" },
  { name: "Cartón mixto", score: "88.6%", status: "Revisión" }
];

export default function ProcessPipeline() {
  return (
    <GlassCard className="overflow-hidden p-0">
      <div className="flex flex-col gap-3 border-b border-white/10 px-5 py-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-lg font-semibold text-white">Flujo de clasificación</h2>
          <p className="text-sm text-emerald-100/58">
            Visión artificial separada del backend operativo.
          </p>
        </div>
        <Badge variant="mint">Activo</Badge>
      </div>
      <div className="relative h-80 overflow-hidden scanner-surface">
        <motion.div
          className="absolute left-0 right-0 top-8 h-1 bg-mint/80 shadow-glow"
          animate={{ y: [0, 236, 0] }}
          transition={{ duration: 3.8, repeat: Infinity, ease: "easeInOut" }}
        />
        <div className="absolute inset-x-5 bottom-5 grid gap-3 sm:grid-cols-3">
          {streams.map((stream) => (
            <div
              key={stream.name}
              className="rounded-lg border border-white/12 bg-graphite/72 p-4 backdrop-blur"
            >
              <div className="flex items-center gap-2">
                <CheckCircle2 className="text-mint" size={16} aria-hidden="true" />
                <p className="text-sm font-semibold text-white">{stream.name}</p>
              </div>
              <p className="mt-3 text-2xl font-semibold text-mint">{stream.score}</p>
              <p className="mt-1 text-xs text-emerald-100/60">{stream.status}</p>
            </div>
          ))}
        </div>
      </div>
    </GlassCard>
  );
}
