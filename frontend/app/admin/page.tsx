export default function AdminDashboard() {
  const stats = [
    { n: "4,218", l: "Students" },
    { n: "226", l: "Teachers" },
    { n: "9", l: "Sub-Admins" },
    { n: "₹38L", l: "Fees Due" },
  ];
  return (
    <>
      <h1 className="font-display text-3xl font-black text-maroon">Admin Dashboard</h1>
      <p className="mt-1 text-ink/60">Everything happening across the institute, today.</p>
      <div className="mt-6 grid grid-cols-2 gap-4 md:grid-cols-4">
        {stats.map((s) => (
          <div key={s.l} className="rounded-2xl border border-ink/10 bg-white p-5 shadow-sm">
            <p className="font-display text-3xl font-black text-maroon">{s.n}</p>
            <p className="text-xs tracking-widest text-ink/50">{s.l}</p>
          </div>
        ))}
      </div>
      <h2 className="mt-10 font-display text-xl font-bold">Recent Activity</h2>
      <ul className="mt-4 space-y-3">
        {[
          "Accountant role updated for Priya Sen",
          "42 new admission applications pending review",
          "Attendance synced for CSE-3A by Prof. Ghosh",
          "Gallery updated: TechFest 2026 album",
        ].map((a) => (
          <li key={a} className="rounded-xl border border-ink/10 bg-white px-4 py-3 text-sm">
            {a}
          </li>
        ))}
      </ul>
    </>
  );
}
