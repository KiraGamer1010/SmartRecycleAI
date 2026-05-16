import { motion } from "framer-motion";
import { cn } from "../../utils/cn.js";

export default function GlassCard({
  as: Component = motion.article,
  children,
  className,
  delay = 0,
  ...props
}) {
  return (
    <Component
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.45, delay, ease: "easeOut" }}
      className={cn("glass-panel p-5", className)}
      {...props}
    >
      {children}
    </Component>
  );
}
