import { motion } from "framer-motion";
import { Camera, CheckCircle2, UploadCloud } from "lucide-react";
import SectionHeader from "../components/common/SectionHeader.jsx";
import StatusBadge from "../components/common/StatusBadge.jsx";

export default function RecognitionPage() {
  return (
    <div className="space-y-6">
      <SectionHeader eyebrow="Vision IA" title="Reconocimiento de materiales" />
      <section className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-lg border border-white/10 bg-panel/86 p-5"
        >
          <div className="flex items-center gap-3">
            <span className="rounded-lg border border-mint/25 bg-mint/10 p-3 text-mint">
              <UploadCloud aria-hidden="true" size={24} />
            </span>
            <div>
              <h2 className="text-lg font-semibold text-white">
                Entrada de imagen
              </h2>
              <p className="text-sm text-emerald-100/58">
                Preparado para integrar carga de imagen y camara industrial.
              </p>
            </div>
          </div>
          <div className="mt-6 flex min-h-72 items-center justify-center rounded-lg border border-dashed border-mint/30 bg-mint/5 p-6 text-center">
            <div>
              <Camera className="mx-auto text-mint" size={42} aria-hidden="true" />
              <p className="mt-4 text-base font-semibold text-white">
                Canal de deteccion listo
              </p>
              <p className="mt-2 max-w-sm text-sm text-emerald-100/58">
                El motor IA vive en `ai-engine` y se comunica por contrato HTTP.
              </p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.08 }}
          className="rounded-lg border border-white/10 bg-panel/86 p-5"
        >
          <div className="flex items-center justify-between gap-4">
            <div>
              <h2 className="text-lg font-semibold text-white">
                Pipeline de inferencia
              </h2>
              <p className="text-sm text-emerald-100/58">
                Normalizacion, deteccion y salida estructurada.
              </p>
            </div>
            <StatusBadge variant="online">Contrato v1</StatusBadge>
          </div>
          <div className="mt-6 grid gap-3">
            {[
              "Validacion de imagen",
              "Modelo YOLO cargado bajo demanda",
              "Respuesta normalizada para API"
            ].map((step) => (
              <div
                key={step}
                className="flex items-center gap-3 rounded-lg border border-white/10 bg-white/[0.04] px-4 py-3"
              >
                <CheckCircle2 className="text-mint" size={18} aria-hidden="true" />
                <span className="text-sm text-emerald-50/82">{step}</span>
              </div>
            ))}
          </div>
        </motion.div>
      </section>
    </div>
  );
}
