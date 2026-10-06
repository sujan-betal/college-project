import PageBanner from "@/components/PageBanner";

const depts = [
  ["Computer Science & Engineering", "AI, cybersecurity, and software systems labs."],
  ["Electronics & Communication", "VLSI, embedded systems, and signal processing."],
  ["Mechanical Engineering", "Design, thermal, and manufacturing excellence."],
  ["Data Science", "Statistics, ML, and decision sciences."],
  ["Business Administration", "Finance, analytics, and entrepreneurship."],
  ["Basic Sciences & Humanities", "The foundation of analytical thinking."],
];

export default function Departments() {
  return (
    <>
      <PageBanner kicker="OUR SCHOOLS" title="Departments" text="Six schools, one campus — each with dedicated labs, faculty, and placement cells." />
      <section className="mx-auto grid max-w-6xl gap-4 px-4 py-14 md:grid-cols-3">
        {depts.map(([name, desc]) => (
          <div key={name} className="rounded-2xl border border-ink/10 bg-white p-6 hover:-translate-y-1 hover:shadow-md transition">
            <h3 className="font-display text-lg font-bold text-maroon">{name}</h3>
            <p className="mt-2 text-sm text-ink/60">{desc}</p>
          </div>
        ))}
      </section>
    </>
  );
}
