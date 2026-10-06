export default function ModulePage({
  title,
  desc,
  stats,
  columns,
  rows,
}: {
  title: string;
  desc: string;
  stats: { n: string; l: string }[];
  columns: string[];
  rows: string[][];
}) {
  return (
    <>
      <h1 className="font-display text-3xl font-black text-maroon">{title}</h1>
      <p className="mt-1 text-ink/80">{desc}</p>
      <div className="mt-6 grid grid-cols-2 gap-4 md:grid-cols-4">
        {stats.map((s) => (
          <div key={s.l} className="rounded-2xl border border-ink/10 bg-white p-4 text-center shadow-sm">
            <p className="font-display text-2xl font-black text-maroon">{s.n}</p>
            <p className="text-xs tracking-widest text-ink/50">{s.l}</p>
          </div>
        ))}
      </div>
      <div className="mt-8 overflow-x-auto rounded-2xl border border-ink/10 bg-white shadow-sm">
        <table className="w-full min-w-[560px] text-sm">
          <thead>
            <tr className="bg-maroon text-cream">
              {columns.map((c) => (
                <th key={c} className="px-4 py-3 text-left font-semibold">{c}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={i} className={i % 2 ? "bg-cream/60" : ""}>
                {r.map((cell, j) => (
                  <td key={j} className="px-4 py-3">{cell}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="mt-3 text-xs text-ink/40">
        Design preview — data connects to the backend later.
      </p>
    </>
  );
}
