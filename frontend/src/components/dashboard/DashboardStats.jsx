import { Database, Gauge, Leaf, Recycle } from "lucide-react";
import StatCard from "../ui/StatCard.jsx";

const stats = [
  {
    icon: Recycle,
    label: "Material procesado",
    value: "12.8 t",
    detail: "Metrica operacional inicial para plantas piloto.",
    tone: "mint"
  },
  {
    icon: Gauge,
    label: "Precision estimada",
    value: "96.2%",
    detail: "Indicador objetivo para visión computacional.",
    tone: "signal"
  },
  {
    icon: Leaf,
    label: "Desvio evitado",
    value: "8.4 t",
    detail: "Impacto ambiental proyectado.",
    tone: "solar"
  },
  {
    icon: Database,
    label: "Datos trazables",
    value: "MLOps",
    detail: "Versionamiento, monitoreo y documentación.",
    tone: "mint"
  }
];

export default function DashboardStats() {
  return (
    <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
      {stats.map((stat) => (
        <StatCard key={stat.label} {...stat} />
      ))}
    </section>
  );
}
