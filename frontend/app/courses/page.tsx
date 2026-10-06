import PageBanner from "@/components/PageBanner";

const courses = [
  { name: "B.Tech — Computer Science & AI", seats: 120, duration: "4 yrs", fee: "₹1.1L/yr" },
  { name: "B.Tech — Mechanical Engineering", seats: 90, duration: "4 yrs", fee: "₹95k/yr" },
  { name: "B.Sc — Data Science", seats: 60, duration: "3 yrs", fee: "₹70k/yr" },
  { name: "BBA — Finance & Analytics", seats: 60, duration: "3 yrs", fee: "₹80k/yr" },
  { name: "M.Tech — VLSI Design", seats: 24, duration: "2 yrs", fee: "₹1.4L/yr" },
  { name: "MBA — Business Analytics", seats: 40, duration: "2 yrs", fee: "₹1.6L/yr" },
];

export default function Courses() {
  return (
    <>
      <PageBanner
        kicker="ACADEMICS"
        title="Courses & Programs"
        text="Industry-aligned programs with mandatory internships, live projects, and a credit system built for flexibility."
      />
      <section className="mx-auto grid max-w-6xl gap-4 px-4 py-14 md:grid-cols-2">
        {courses.map((c) => (
          <div
            key={c.name}
            className="rounded-2xl border border-ink/10 bg-white p-6 hover:-translate-y-1 hover:shadow-md transition"
          >
            <h3 className="font-display text-xl font-bold text-maroon">{c.name}</h3>
            <div className="mt-4 flex gap-3 text-xs">
              <span className="rounded-full bg-cream px-3 py-1">{c.seats} seats</span>
              <span className="rounded-full bg-cream px-3 py-1">{c.duration}</span>
              <span className="rounded-full bg-saffron-soft px-3 py-1 font-semibold">{c.fee}</span>
            </div>
          </div>
        ))}
      </section>
    </>
  );
}
