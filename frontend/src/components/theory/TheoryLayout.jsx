import TheorySidebar from "./TheorySidebar.jsx";

export default function TheoryLayout({ children, sections }) {
  return (
    <div className="grid gap-6 xl:grid-cols-[300px_minmax(0,1fr)]">
      <TheorySidebar sections={sections} />
      <div className="min-w-0 space-y-5">{children}</div>
    </div>
  );
}
