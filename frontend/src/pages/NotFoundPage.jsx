import { Link } from "react-router-dom";
import Button from "../components/ui/Button.jsx";

export default function NotFoundPage() {
  return (
    <section className="glass-panel p-8 text-center">
      <h1 className="text-3xl font-semibold text-white">Vista no encontrada</h1>
      <p className="mt-3 text-emerald-100/62">
        La ruta solicitada no pertenece al modulo operativo actual.
      </p>
      <Button as={Link} className="mt-6" to="/">
        Volver al panel
      </Button>
    </section>
  );
}
