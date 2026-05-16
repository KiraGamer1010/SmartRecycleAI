import { motion } from "framer-motion";
import { cn } from "../../utils/cn.js";

export default function MotionSection({ children, className, delay = 0, ...props }) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 18 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.5, delay, ease: "easeOut" }}
      className={cn(className)}
      {...props}
    >
      {children}
    </motion.section>
  );
}
