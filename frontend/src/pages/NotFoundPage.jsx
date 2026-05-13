import { Link } from "react-router-dom";

export default function NotFoundPage() {
  return (
    <section className="rounded-lg border border-white/10 bg-panel/86 p-8 text-center">
      <h1 className="text-3xl font-semibold text-white">Vista no encontrada</h1>
      <p className="mt-3 text-emerald-100/62">
        La ruta solicitada no pertenece al modulo operativo actual.
      </p>
      <Link
        className="mt-6 inline-flex rounded-lg bg-mint px-4 py-2 text-sm font-semibold text-graphite"
        to="/"
      >
        Volver al panel
      </Link>
    </section>
  );
}
