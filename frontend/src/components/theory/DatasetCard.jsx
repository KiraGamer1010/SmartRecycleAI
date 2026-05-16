import { Database } from "lucide-react";

export default function DatasetCard({ title, items }) {
  return (
    <div className="rounded-lg border border-signal/20 bg-signal/10 p-4">
      <div className="flex items-center gap-3">
        <span className="rounded-lg border border-signal/25 bg-signal/10 p-2 text-signal">
          <Database size={18} aria-hidden="true" />
        </span>
        <h3 className="text-sm font-semibold text-white">{title}</h3>
      </div>
      <ul className="mt-4 space-y-2 text-sm leading-6 text-emerald-50/72">
        {items.map((item) => (
          <li key={item} className="flex gap-2">
            <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-signal" />
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
