export default function StudentOverview() {
  const stats = [
    { n: "91%", l: "ATTENDANCE" },
    { n: "8.1", l: "CGPA" },
    { n: "₹22k", l: "FEES DUE" },
    { n: "3", l: "ASSIGNMENTS" },
  ];
  return (
    <>
      <h1 className="font-display text-3xl font-black text-maroon">Hi, Aarav</h1>
      <p className="mt-1 text-ink/60">Semester 3 · B.Tech CSE · Section 3A</p>
      <div className="mt-6 grid grid-cols-2 gap-4 md:grid-cols-4">
        {stats.map((s) => (
          <div key={s.l} className="rounded-2xl border border-ink/10 bg-white p-5 shadow-sm">
            <p className="font-display text-3xl font-black text-maroon">{s.n}</p>
            <p className="text-xs tracking-widest text-ink/50">{s.l}</p>
          </div>
        ))}
      </div>
      <h2 className="mt-10 font-display text-xl font-bold">Today&apos;s Classes</h2>
      <ul className="mt-4 space-y-3">
        {["10:00 — VLSI (Lab 2)", "12:30 — Digital Logic", "14:00 — Discrete Math"].map((a) => (
          <li key={a} className="rounded-xl border border-ink/10 bg-white px-4 py-3 text-sm">{a}</li>
        ))}
      </ul>
    </>
  );
}
