import { AlertTriangle } from "lucide-react";

export default function RiskCard({ title, items }) {
  return (
    <div className="rounded-lg border border-solar/20 bg-solar/10 p-4">
      <div className="flex items-center gap-3">
        <AlertTriangle className="text-solar" size={18} aria-hidden="true" />
        <h3 className="text-sm font-semibold text-white">{title}</h3>
      </div>
      <ul className="mt-4 space-y-2 text-sm leading-6 text-emerald-50/72">
        {items.map((item) => (
          <li key={item} className="flex gap-2">
            <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-solar" />
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
