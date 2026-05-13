import { motion } from "framer-motion";

export default function MetricCard({ icon: Icon, label, value, tone = "mint" }) {
  const toneClass = {
    mint: "text-mint bg-mint/10 border-mint/25",
    signal: "text-signal bg-signal/10 border-signal/25",
    solar: "text-solar bg-solar/10 border-solar/25"
  }[tone];

  return (
    <motion.article
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-lg border border-white/10 bg-white/[0.045] p-4 shadow-glow"
    >
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm text-emerald-100/62">{label}</p>
          <strong className="mt-2 block text-2xl font-semibold text-white">
            {value}
          </strong>
        </div>
        <span className={`rounded-lg border p-3 ${toneClass}`}>
          <Icon aria-hidden="true" size={22} />
        </span>
      </div>
    </motion.article>
  );
}
