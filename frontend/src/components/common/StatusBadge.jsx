const variants = {
  online: "border-mint/30 bg-mint/10 text-mint",
  warning: "border-solar/30 bg-solar/10 text-solar",
  neutral: "border-white/15 bg-white/10 text-emerald-50/80"
};

export default function StatusBadge({ children, variant = "neutral" }) {
  return (
    <span
      className={`inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-medium ${variants[variant]}`}
    >
      <span className="h-2 w-2 rounded-full bg-current" />
      {children}
    </span>
  );
}
