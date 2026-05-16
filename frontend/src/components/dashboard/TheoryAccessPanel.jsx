import { ArrowRight, BookOpenText } from "lucide-react";
import { Link } from "react-router-dom";
import Button from "../ui/Button.jsx";
import GlassCard from "../ui/GlassCard.jsx";

export default function TheoryAccessPanel() {
  return (
    <GlassCard className="flex flex-col gap-5 border-mint/20 bg-mint/10 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex items-start gap-4">
        <span className="rounded-lg border border-mint/25 bg-mint/10 p-3 text-mint">
          <BookOpenText size={24} aria-hidden="true" />
        </span>
        <div>
          <h2 className="text-lg font-semibold text-white">
            Documentación teórica de Machine Learning
          </h2>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-emerald-50/68">
            Accede a la base académica del proyecto: negocio, datos, viabilidad,
            riesgos, transformaciones, MLOps y referencias bibliográficas.
          </p>
        </div>
      </div>
      <Button as={Link} to="/theory" className="shrink-0">
        Ver teoría
        <ArrowRight size={18} aria-hidden="true" />
      </Button>
    </GlassCard>
  );
}
