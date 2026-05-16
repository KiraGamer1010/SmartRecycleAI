import { ExternalLink } from "lucide-react";

function extractUrl(reference) {
  return reference.match(/https?:\/\/\S+/)?.[0] ?? "";
}

export default function ReferenceCard({ reference, index }) {
  const url = extractUrl(reference);

  return (
    <article className="rounded-lg border border-white/10 bg-white/[0.045] p-4">
      <div className="flex items-start gap-3">
        <span className="grid h-8 w-8 shrink-0 place-items-center rounded-lg border border-mint/25 bg-mint/10 text-xs font-semibold text-mint">
          {index + 1}
        </span>
        <div className="min-w-0">
          <p className="text-sm leading-6 text-emerald-50/78">{reference}</p>
          {url ? (
            <a
              className="focus-ring mt-3 inline-flex items-center gap-2 rounded-lg text-sm font-medium text-mint hover:text-emerald-200"
              href={url}
              rel="noreferrer"
              target="_blank"
            >
              Abrir fuente
              <ExternalLink size={15} aria-hidden="true" />
            </a>
          ) : null}
        </div>
      </div>
    </article>
  );
}
