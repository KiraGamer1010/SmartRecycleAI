import { useMemo } from "react";
import { BookOpenText } from "lucide-react";
import { useActiveSection } from "../../hooks/useActiveSection.js";
import { cn } from "../../utils/cn.js";
import Badge from "../ui/Badge.jsx";

export default function TheorySidebar({ sections }) {
  const sectionIds = useMemo(() => sections.map((section) => section.id), [sections]);
  const activeId = useActiveSection(sectionIds);

  return (
    <aside className="glass-panel p-4 lg:sticky lg:top-24 lg:max-h-[calc(100vh-7.5rem)] lg:overflow-auto">
      <div className="flex items-center gap-3">
        <span className="rounded-lg border border-mint/25 bg-mint/10 p-2 text-mint">
          <BookOpenText size={18} aria-hidden="true" />
        </span>
        <div>
          <p className="text-sm font-semibold text-white">Machine Learning Theory</p>
          <p className="text-xs text-emerald-100/55">Indice academico</p>
        </div>
      </div>
      <Badge className="mt-4" variant="mint">
        {sections.length} secciones
      </Badge>

      <nav className="mt-5 grid gap-1" aria-label="Índice de teoría">
        {sections.map((section) => (
          <a
            key={section.id}
            className={cn(
              "focus-ring rounded-lg px-3 py-2 text-sm transition",
              activeId === section.id
                ? "bg-mint text-graphite"
                : "text-emerald-50/68 hover:bg-white/[0.08] hover:text-white"
            )}
            href={`#${section.id}`}
          >
            <span className="mr-2 text-xs font-semibold opacity-70">
              {section.number}
            </span>
            {section.title}
          </a>
        ))}
      </nav>
    </aside>
  );
}
