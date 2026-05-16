export default function TimelineML({ items }) {
  return (
    <div className="relative space-y-4">
      <div className="absolute bottom-4 left-4 top-4 w-px bg-mint/20" />
      {items.map((item, index) => (
        <div key={item.title} className="relative flex gap-4">
          <span className="z-10 grid h-8 w-8 shrink-0 place-items-center rounded-full border border-mint/30 bg-graphite text-xs font-semibold text-mint">
            {index + 1}
          </span>
          <div className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
            <h3 className="text-sm font-semibold text-white">{item.title}</h3>
            <p className="mt-2 text-sm leading-6 text-emerald-50/66">{item.detail}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
