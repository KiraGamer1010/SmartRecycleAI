export default function SectionHeader({ eyebrow, title, action }) {
  return (
    <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
      <div>
        {eyebrow ? (
          <p className="text-xs font-semibold uppercase text-mint/80">
            {eyebrow}
          </p>
        ) : null}
        <h1 className="mt-2 text-3xl font-semibold text-white sm:text-4xl">
          {title}
        </h1>
      </div>
      {action}
    </div>
  );
}
