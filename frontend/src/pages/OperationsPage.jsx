import { motion } from "framer-motion";
import { AlertTriangle, Database, Factory, ShieldCheck } from "lucide-react";
import SectionHeader from "../components/common/SectionHeader.jsx";
import StatusBadge from "../components/common/StatusBadge.jsx";

const rows = [
  ["Linea norte", "PET", "96.8%", "Normal"],
  ["Linea sur", "Vidrio", "91.2%", "Normal"],
  ["Linea oeste", "Mixto", "78.4%", "Revision"]
];

export default function OperationsPage() {
  return (
    <div className="space-y-6">
      <SectionHeader eyebrow="Operaciones" title="Supervision de planta" />
      <section className="grid gap-6 lg:grid-cols-[1fr_320px]">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="overflow-hidden rounded-lg border border-white/10 bg-panel/86"
        >
          <div className="flex items-center justify-between border-b border-white/10 px-5 py-4">
            <div className="flex items-center gap-3">
              <Factory className="text-mint" size={22} aria-hidden="true" />
              <h2 className="text-lg font-semibold text-white">
                Lineas de clasificacion
              </h2>
            </div>
            <StatusBadge variant="online">Monitoreo</StatusBadge>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-white/10 text-left text-sm">
              <thead className="bg-white/[0.04] text-emerald-100/60">
                <tr>
                  <th className="px-5 py-3 font-medium">Linea</th>
                  <th className="px-5 py-3 font-medium">Material</th>
                  <th className="px-5 py-3 font-medium">Confianza</th>
                  <th className="px-5 py-3 font-medium">Estado</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/10">
                {rows.map(([line, material, confidence, status]) => (
                  <tr key={line} className="text-emerald-50/82">
                    <td className="px-5 py-4">{line}</td>
                    <td className="px-5 py-4">{material}</td>
                    <td className="px-5 py-4">{confidence}</td>
                    <td className="px-5 py-4">
                      <StatusBadge
                        variant={status === "Revision" ? "warning" : "online"}
                      >
                        {status}
                      </StatusBadge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>

        <motion.aside
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.08 }}
          className="space-y-4"
        >
          <div className="rounded-lg border border-white/10 bg-panel/86 p-5">
            <Database className="text-signal" size={24} aria-hidden="true" />
            <h2 className="mt-4 text-lg font-semibold text-white">
              Datos persistentes
            </h2>
            <p className="mt-2 text-sm text-emerald-100/58">
              PostgreSQL queda como fuente operativa principal.
            </p>
          </div>
          <div className="rounded-lg border border-white/10 bg-panel/86 p-5">
            <ShieldCheck className="text-mint" size={24} aria-hidden="true" />
            <h2 className="mt-4 text-lg font-semibold text-white">
              Separacion limpia
            </h2>
            <p className="mt-2 text-sm text-emerald-100/58">
              Cada modulo tiene dependencias, pruebas y despliegue propio.
            </p>
          </div>
          <div className="rounded-lg border border-solar/20 bg-solar/10 p-5">
            <AlertTriangle className="text-solar" size={24} aria-hidden="true" />
            <h2 className="mt-4 text-lg font-semibold text-white">
              Acciones pendientes
            </h2>
            <p className="mt-2 text-sm text-emerald-100/68">
              Entrenar modelo productivo y conectar camaras reales.
            </p>
          </div>
        </motion.aside>
      </section>
    </div>
  );
}
