import { BookOpenText, CalendarDays, GraduationCap, Users } from "lucide-react";
import TheoryLayout from "../components/theory/TheoryLayout.jsx";
import TheorySection from "../components/theory/TheorySection.jsx";
import Badge from "../components/ui/Badge.jsx";
import GlassCard from "../components/ui/GlassCard.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import StatCard from "../components/ui/StatCard.jsx";
import {
  theoryDocument,
  theorySections,
  theoryStats
} from "../utils/mlTheoryContent.js";

const statIcons = [BookOpenText, GraduationCap, Users, CalendarDays];

export default function TheoryPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Machine Learning Theory"
        title="Teoría académica y técnica de SmartRecycleAI"
        description="Documentación completa del proyecto de Machine Learning: entendimiento del negocio, datos, viabilidad, tecnologías, riesgos, ingeniería de datos, transformaciones, conclusiones y referencias bibliográficas."
      />

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {theoryStats.map((stat, index) => (
          <StatCard
            key={stat.label}
            icon={statIcons[index]}
            label={stat.label}
            value={stat.value}
            tone={index === 1 ? "signal" : index === 3 ? "solar" : "mint"}
          />
        ))}
      </section>

      <GlassCard className="grid gap-4 md:grid-cols-[1fr_1.25fr]">
        <div>
          <Badge variant="mint">{theoryDocument.deliverable}</Badge>
          <h2 className="mt-4 text-2xl font-semibold text-white">
            {theoryDocument.project}
          </h2>
          <p className="mt-3 text-sm leading-6 text-emerald-50/68">
            Asignatura: {theoryDocument.course}. Universidad:{" "}
            {theoryDocument.university}. Sede: {theoryDocument.campus}. Fecha:{" "}
            {theoryDocument.date}.
          </p>
        </div>
        <div className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
          <p className="text-sm font-semibold text-white">Autores</p>
          <div className="mt-3 grid gap-2 sm:grid-cols-2">
            {theoryDocument.authors.map((author) => (
              <div
                key={author}
                className="rounded-lg border border-white/10 bg-graphite/44 px-3 py-2 text-sm text-emerald-50/76"
              >
                {author}
              </div>
            ))}
          </div>
        </div>
      </GlassCard>

      <TheoryLayout sections={theorySections}>
        {theorySections.map((section) => (
          <TheorySection key={section.id} section={section} />
        ))}
      </TheoryLayout>
    </div>
  );
}
