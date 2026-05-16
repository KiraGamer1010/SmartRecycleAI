import { Cpu } from "lucide-react";
import TheoryCard from "./TheoryCard.jsx";

export default function TechnologyGrid({ groups }) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      {groups.map((group) => (
        <TheoryCard
          key={group.title}
          title={
            <span className="inline-flex items-center gap-2">
              <Cpu className="text-mint" size={17} aria-hidden="true" />
              {group.title}
            </span>
          }
          items={group.items}
        />
      ))}
    </div>
  );
}
