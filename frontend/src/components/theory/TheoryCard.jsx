import GlassCard from "../ui/GlassCard.jsx";

export default function TheoryCard({ title, body, items }) {
  return (
    <GlassCard className="p-4">
      <h3 className="text-sm font-semibold text-white">{title}</h3>
      {body ? (
        <p className="mt-2 text-sm leading-6 text-emerald-50/66">{body}</p>
      ) : null}
      {items?.length ? (
        <ul className="mt-3 space-y-2 text-sm leading-6 text-emerald-50/66">
          {items.map((item) => (
            <li key={item} className="flex gap-2">
              <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-mint" />
              <span>{item}</span>
            </li>
          ))}
        </ul>
      ) : null}
    </GlassCard>
  );
}
