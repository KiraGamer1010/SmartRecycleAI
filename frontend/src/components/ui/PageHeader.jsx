import Badge from "./Badge.jsx";

export default function PageHeader({ eyebrow, title, description, action }) {
  return (
    <header className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
      <div className="max-w-3xl">
        {eyebrow ? <Badge variant="mint">{eyebrow}</Badge> : null}
        <h1 className="mt-4 text-3xl font-semibold text-white sm:text-4xl lg:text-5xl">
          {title}
        </h1>
        {description ? (
          <p className="mt-4 text-base leading-7 text-emerald-50/68">
            {description}
          </p>
        ) : null}
      </div>
      {action ? <div className="flex shrink-0 flex-wrap gap-3">{action}</div> : null}
    </header>
  );
}
