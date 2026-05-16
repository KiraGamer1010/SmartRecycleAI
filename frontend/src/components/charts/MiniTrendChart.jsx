const values = [48, 64, 58, 78, 86, 74, 92, 88, 96, 91, 98, 94];

export default function MiniTrendChart() {
  return (
    <div
      className="flex h-32 items-end gap-2 rounded-lg border border-white/10 bg-graphite/56 p-4"
      aria-label="Tendencia visual de eficiencia operacional"
    >
      {values.map((value, index) => (
        <span
          key={`${value}-${index}`}
          className="flex-1 rounded-t bg-gradient-to-t from-algae to-mint"
          style={{ height: `${value}%` }}
        />
      ))}
    </div>
  );
}
