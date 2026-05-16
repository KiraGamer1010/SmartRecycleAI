import GlassCard from "./GlassCard.jsx";

export default function StatCard({ icon: Icon, label, value, detail, tone = "mint" }) {
  const tones = {
    mint: "text-mint bg-mint/10 border-mint/25",
    signal: "text-signal bg-signal/10 border-signal/25",
    solar: "text-solar bg-solar/10 border-solar/25"
  };

  return (
    <GlassCard className="p-4">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm text-emerald-100/62">{label}</p>
          <strong className="mt-2 block text-2xl font-semibold text-white">
            {value}
          </strong>
          {detail ? (
            <p className="mt-2 text-xs leading-5 text-emerald-100/54">{detail}</p>
          ) : null}
        </div>
        <span className={`rounded-lg border p-3 ${tones[tone]}`}>
          <Icon aria-hidden="true" size={22} />
        </span>
      </div>
    </GlassCard>
  );
}
