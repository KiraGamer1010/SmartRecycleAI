import {
  BookOpenText,
  Camera,
  Factory,
  Home,
  LayoutDashboard
} from "lucide-react";

export const navigationItems = [
  { to: "/", label: "Home", icon: Home, end: true },
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/recognition", label: "Visión IA", icon: Camera },
  { to: "/operations", label: "Operaciones", icon: Factory },
  { to: "/theory", label: "Teoría ML", icon: BookOpenText }
];
