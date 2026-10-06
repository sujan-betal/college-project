import PageBanner from "@/components/PageBanner";

const events = [
  ["14 Dec", "Annual Convocation — chief guest Dr. A. Sen"],
  ["02 Nov", "TechFest 2026 — hackathon, robo-war, guest lectures"],
  ["21 Oct", "Career Fair with 60+ recruiters"],
  ["08 Jan", "Semester exams begin"],
];

export default function Events() {
  return (
    <>
      <PageBanner kicker="WHAT'S ON" title="Events" text="From fests to fairs — there is always something happening on campus." />
      <section className="mx-auto max-w-4xl px-4 py-14 space-y-4">
        {events.map(([date, title]) => (
          <div key={title} className="flex flex-col gap-3 rounded-2xl border border-ink/10 bg-white p-5 sm:flex-row sm:items-center sm:gap-5">
            <span className="w-fit rounded-xl bg-maroon px-4 py-2 font-display font-bold text-saffron">{date}</span>
            <p className="font-semibold">{title}</p>
          </div>
        ))}
      </section>
    </>
  );
}
