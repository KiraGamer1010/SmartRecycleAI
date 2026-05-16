import { motion } from "framer-motion";
import { ArrowRight, Cpu, Recycle, ShieldCheck } from "lucide-react";
import { Link } from "react-router-dom";
import Badge from "../ui/Badge.jsx";
import Button from "../ui/Button.jsx";

export default function HeroSection() {
  return (
    <section className="relative min-h-[520px] overflow-hidden rounded-lg border border-white/10 bg-graphite bg-scanner-radial shadow-premium">
      <div className="absolute inset-0 bg-premium-grid bg-[length:44px_44px] opacity-80" />
      <div className="absolute inset-x-0 top-24 h-px bg-mint/35 shadow-glow" />
      <div className="absolute right-8 top-10 hidden h-72 w-72 rounded-full border border-mint/20 lg:block">
        <div className="absolute inset-10 rounded-full border border-signal/20" />
        <div className="absolute inset-24 rounded-full bg-mint/15 shadow-glow" />
      </div>

      <div className="relative z-10 grid min-h-[520px] gap-8 px-5 py-10 sm:px-8 lg:grid-cols-[1.05fr_0.95fr] lg:px-10">
        <div className="flex flex-col justify-center">
          <Badge variant="mint">SmartRecycleAI Machine Learning</Badge>
          <h1 className="mt-6 max-w-3xl text-4xl font-semibold leading-tight text-white sm:text-5xl lg:text-6xl">
            Inteligencia artificial aplicada al reciclaje industrial.
          </h1>
          <p className="mt-5 max-w-2xl text-base leading-7 text-emerald-50/70">
            Plataforma modular para clasificar residuos con visión computacional,
            documentar el ciclo de Machine Learning y preparar operaciones listas
            para MLOps.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Button as={Link} to="/dashboard">
              Abrir dashboard
              <ArrowRight aria-hidden="true" size={18} />
            </Button>
            <Button as={Link} to="/theory" variant="secondary">
              Explorar teoría
            </Button>
          </div>
        </div>

        <div className="flex items-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.96 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.7, ease: "easeOut" }}
            className="w-full rounded-lg border border-white/10 bg-panel/78 p-4 backdrop-blur-xl"
          >
            <div className="grid gap-3 sm:grid-cols-3">
              {[
                { icon: Recycle, label: "Clasificacion", value: "8 clases" },
                { icon: Cpu, label: "Inferencia", value: "YOLO" },
                { icon: ShieldCheck, label: "MLOps", value: "Trazable" }
              ].map(({ icon: Icon, label, value }) => (
                <div
                  key={label}
                  className="rounded-lg border border-white/10 bg-white/[0.055] p-4"
                >
                  <Icon className="text-mint" size={22} aria-hidden="true" />
                  <p className="mt-4 text-xs text-emerald-100/58">{label}</p>
                  <p className="mt-1 text-lg font-semibold text-white">{value}</p>
                </div>
              ))}
            </div>
            <div className="mt-4 h-56 overflow-hidden rounded-lg border border-mint/20 scanner-surface">
              <motion.div
                className="h-1 bg-mint/90 shadow-glow"
                animate={{ y: [18, 206, 18] }}
                transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
              />
              <div className="grid h-full place-items-center px-6 text-center">
                <p className="max-w-sm text-sm leading-6 text-emerald-50/72">
                  Flujo visual preparado para imagenes, detecciones y datos
                  ambientales en tiempo real.
                </p>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
