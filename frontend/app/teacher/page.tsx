export default function TeacherOverview() {
  const stats = [
    { n: "4", l: "SUBJECTS" },
    { n: "3", l: "SECTIONS" },
    { n: "118", l: "STUDENTS" },
    { n: "92%", l: "AVG ATTEND." },
  ];
  return (
    <>
      <h1 className="font-display text-3xl font-black text-maroon">Welcome, Prof. Ghosh</h1>
      <p className="mt-1 text-ink/60">Your classes, subjects, and today&apos;s schedule at a glance.</p>
      <div className="mt-6 grid grid-cols-2 gap-4 md:grid-cols-4">
        {stats.map((s) => (
          <div key={s.l} className="rounded-2xl border border-ink/10 bg-white p-5 shadow-sm">
            <p className="font-display text-3xl font-black text-maroon">{s.n}</p>
            <p className="text-xs tracking-widest text-ink/50">{s.l}</p>
          </div>
        ))}
      </div>
      <h2 className="mt-10 font-display text-xl font-bold">Today</h2>
      <ul className="mt-4 space-y-3">
        {["10:00 — VLSI, CSE-3A (Lab 2)", "12:30 — NLP, CSE-5B", "14:00 — Office hours"].map((a) => (
          <li key={a} className="rounded-xl border border-ink/10 bg-white px-4 py-3 text-sm">{a}</li>
        ))}
      </ul>
    </>
  );
}
