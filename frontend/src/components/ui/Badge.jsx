import { cn } from "../../utils/cn.js";

const variants = {
  mint: "border-mint/30 bg-mint/10 text-mint",
  signal: "border-signal/30 bg-signal/10 text-signal",
  solar: "border-solar/30 bg-solar/10 text-solar",
  neutral: "border-white/15 bg-white/10 text-emerald-50/78"
};

export default function Badge({ children, className, variant = "neutral" }) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-medium",
        variants[variant],
        className
      )}
    >
      {children}
    </span>
  );
}
