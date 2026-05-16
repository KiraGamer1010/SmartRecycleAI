import { cn } from "../../utils/cn.js";

const variants = {
  primary: "bg-mint text-graphite hover:bg-emerald-300",
  secondary:
    "border border-white/12 bg-white/[0.06] text-emerald-50 hover:bg-white/[0.1]",
  ghost: "text-emerald-50/78 hover:bg-white/[0.08] hover:text-white"
};

export default function Button({
  as: Component = "button",
  children,
  className,
  variant = "primary",
  ...props
}) {
  return (
    <Component
      className={cn(
        "focus-ring inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2 text-sm font-semibold transition",
        variants[variant],
        className
      )}
      {...props}
    >
      {children}
    </Component>
  );
}
