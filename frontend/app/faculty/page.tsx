import PageBanner from "@/components/PageBanner";

const faculty = [
  { name: "Dr. Meera Iyer", dept: "CSE — AI & ML", exp: "18 yrs" },
  { name: "Prof. Arindam Ghosh", dept: "ECE — VLSI", exp: "14 yrs" },
  { name: "Dr. Sana Qureshi", dept: "Data Science", exp: "11 yrs" },
  { name: "Prof. Vikram Rao", dept: "Mechanical", exp: "20 yrs" },
  { name: "Dr. Lakshmi Nair", dept: "MBA — Analytics", exp: "16 yrs" },
  { name: "Prof. Rohan Dutta", dept: "Basic Sciences", exp: "9 yrs" },
];

export default function Faculty() {
  return (
    <>
      <PageBanner kicker="OUR TEAM" title="Faculty" text="220+ educators and researchers, many published in top-tier journals and invited to global conferences." />
      <section className="mx-auto grid max-w-6xl gap-4 px-4 py-14 sm:grid-cols-2 md:grid-cols-3">
        {faculty.map((f) => (
          <div key={f.name} className="rounded-2xl border border-ink/10 bg-white p-6 hover:-translate-y-1 hover:shadow-md transition">
            <div className="grid h-14 w-14 place-items-center rounded-full bg-maroon font-display text-xl font-black text-saffron">
              {f.name.split(" ").pop()![0]}
            </div>
            <h3 className="mt-4 font-display text-lg font-bold text-maroon">{f.name}</h3>
            <p className="text-sm text-ink/60">{f.dept}</p>
            <p className="mt-1 text-xs text-ink/40">{f.exp} experience</p>
          </div>
        ))}
      </section>
    </>
  );
}
