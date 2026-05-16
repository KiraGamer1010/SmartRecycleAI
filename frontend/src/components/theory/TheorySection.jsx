import { useState } from "react";
import { ChevronDown } from "lucide-react";
import { motion } from "framer-motion";
import { cn } from "../../utils/cn.js";
import Badge from "../ui/Badge.jsx";
import DatasetCard from "./DatasetCard.jsx";
import ReferenceCard from "./ReferenceCard.jsx";
import RiskCard from "./RiskCard.jsx";
import TechnologyGrid from "./TechnologyGrid.jsx";
import TheoryCard from "./TheoryCard.jsx";
import TimelineML from "./TimelineML.jsx";

export default function TheorySection({ section }) {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <motion.section
      id={section.id}
      initial={{ opacity: 0, y: 18 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.45, ease: "easeOut" }}
      className="scroll-mt-28 rounded-lg border border-white/10 bg-panel/86 shadow-premium"
    >
      <button
        aria-controls={`${section.id}-content`}
        aria-expanded={isOpen}
        className="focus-ring flex w-full items-start justify-between gap-4 rounded-lg px-5 py-5 text-left"
        type="button"
        onClick={() => setIsOpen((current) => !current)}
      >
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-3">
            <Badge variant="mint">{section.number}</Badge>
            {section.eyebrow ? (
              <span className="text-xs font-semibold uppercase text-mint/78">
                {section.eyebrow}
              </span>
            ) : null}
          </div>
          <h2 className="mt-3 text-2xl font-semibold text-white">{section.title}</h2>
        </div>
        <ChevronDown
          className={cn("mt-2 shrink-0 text-emerald-50/70 transition", isOpen && "rotate-180")}
          size={22}
          aria-hidden="true"
        />
      </button>

      {isOpen ? (
        <div id={`${section.id}-content`} className="space-y-5 border-t border-white/10 px-5 py-5">
          {section.paragraphs?.length ? (
            <div className="space-y-4 text-sm leading-7 text-emerald-50/72 sm:text-base">
              {section.paragraphs.map((paragraph) => (
                <p key={paragraph}>{paragraph}</p>
              ))}
            </div>
          ) : null}

          {section.bullets?.length ? (
            <ul className="grid gap-3 md:grid-cols-2">
              {section.bullets.map((bullet) => (
                <li
                  key={bullet}
                  className="rounded-lg border border-white/10 bg-white/[0.045] px-4 py-3 text-sm leading-6 text-emerald-50/72"
                >
                  <span className="mr-2 inline-block h-1.5 w-1.5 rounded-full bg-mint align-middle" />
                  {bullet}
                </li>
              ))}
            </ul>
          ) : null}

          {section.cards?.length ? (
            <div className="grid gap-4 md:grid-cols-2">
              {section.cards.map((card) => (
                <TheoryCard key={card.title} {...card} />
              ))}
            </div>
          ) : null}

          {section.groups?.length ? (
            <div className="grid gap-4 md:grid-cols-2">
              {section.groups.map((group) => (
                <TheoryCard key={group.title} title={group.title} items={group.items} />
              ))}
            </div>
          ) : null}

          {section.datasets?.length ? (
            <DatasetCard title="Datasets Públicos Recomendados" items={section.datasets} />
          ) : null}

          {section.technologies?.length ? (
            <TechnologyGrid groups={section.technologies} />
          ) : null}

          {section.risks?.length ? (
            <div className="grid gap-4 md:grid-cols-3">
              {section.risks.map((risk) => (
                <RiskCard key={risk.title} {...risk} />
              ))}
            </div>
          ) : null}

          {section.timeline?.length ? <TimelineML items={section.timeline} /> : null}

          {section.references?.length ? (
            <div className="grid gap-3">
              {section.references.map((reference, index) => (
                <ReferenceCard
                  key={reference}
                  index={index}
                  reference={reference}
                />
              ))}
            </div>
          ) : null}
        </div>
      ) : null}
    </motion.section>
  );
}
