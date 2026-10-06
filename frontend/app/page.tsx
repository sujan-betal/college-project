import Link from "next/link";
import CountUp from "@/components/CountUp";

const notices = [
  "Admissions Open 2026–27: Apply before 30 November",
  "Annual Convocation on 14 December — chief guest Dr. A. Sen",
  "Semester exams begin 8 January; schedule out",
  "Scholarship applications close 20 October",
];

const stats = [
  { n: "4,200+", l: "Students" },
  { n: "38", l: "Programs" },
  { n: "220+", l: "Faculty" },
  { n: "1998", l: "Est." },
];

const highlights = [
  { title: "TechFest 2026 — 1,800 participants", tag: "Event" },
  { title: "3 patents filed by CSE students", tag: "Achievement" },
  { title: "Top 12% placements, median ₹7.2 LPA", tag: "Placement" },
  { title: "New AI & ML lab inaugurated", tag: "Campus" },
];

export default function Home() {
  return (
    <>
      {/* Notice ticker */}
      <div className="overflow-hidden bg-ink text-saffron-soft">
        <div className="flex w-max animate-marquee gap-12 px-6 py-2 text-sm">
          {[...notices, ...notices].map((n, i) => (
            <span key={i}>✦ {n}</span>
          ))}
        </div>
      </div>

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-br from-maroon-dark via-maroon to-[#93355c] text-white">
        <span className="outline-text absolute -right-6 top-6 hidden font-display text-[10rem] font-black leading-none md:block">
          1998
        </span>
        <div className="relative mx-auto max-w-6xl px-4 py-16 md:py-32">
          <p className="inline-block rounded-full bg-saffron px-4 py-1 text-xs font-bold tracking-[0.3em] text-maroon-dark md:text-sm">
            NAAC A++ · ESTD 1998
          </p>
          <h1 className="mt-6 font-display text-4xl font-black leading-tight sm:text-5xl md:text-7xl">
            Ignite.<br />Innovate.<br />
            <span className="bg-gradient-to-r from-saffron to-saffron-soft bg-clip-text text-transparent">Excel.</span>
          </h1>
          <p className="mt-6 max-w-xl text-lg text-white/90">
            AstraVidya blends rigorous academics with hands-on labs, research
            culture, and industry projects — shaping graduates ready for what&apos;s
            next.
          </p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:gap-4">
            <Link
              href="/admissions"
              className="rounded-full bg-saffron px-8 py-3 text-center font-semibold text-maroon-dark shadow-[0_8px_30px_rgba(240,168,50,0.45)] hover:-translate-y-0.5 hover:brightness-110 transition"
            >
              Apply Now →
            </Link>
            <Link
              href="/courses"
              className="rounded-full border border-cream/40 px-8 py-3 text-center hover:-translate-y-0.5 hover:border-saffron hover:text-saffron transition"
            >
              Explore Courses
            </Link>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="dot-grid">
        <div className="mx-auto grid max-w-6xl grid-cols-2 gap-6 px-4 py-14 md:grid-cols-4">
          {stats.map((s) => (
            <div key={s.l} className="rounded-2xl border-b-4 border-saffron bg-white p-5 text-center shadow-sm">
              <p className="font-display text-4xl font-black text-maroon"><CountUp value={s.n} /></p>
              <p className="mt-1 text-sm tracking-widest text-ink/60">{s.l}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Highlights */}
      <section className="mx-auto max-w-6xl px-4 pb-16">
        <h2 className="font-display text-3xl font-bold">Campus Highlights</h2>
        <div className="mt-6 grid gap-4 md:grid-cols-2">
          {highlights.map((h) => (
            <div
              key={h.title}
              className="rounded-2xl border-l-4 border-maroon bg-white p-6 shadow-sm hover:-translate-y-1 hover:shadow-lg transition"
            >
              <span className="rounded-full bg-saffron-soft px-3 py-0.5 text-xs font-semibold text-maroon">
                {h.tag}
              </span>
              <p className="mt-3 font-semibold">{h.title}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="bg-gradient-to-r from-teal to-[#0b5252] text-white">
        <div className="mx-auto flex max-w-6xl flex-col items-center gap-5 px-4 py-20 text-center">
          <h2 className="font-display text-3xl font-black md:text-5xl">
            Your future starts here.
          </h2>
          <Link
            href="/admissions"
            className="rounded-full bg-saffron px-10 py-3.5 font-semibold text-maroon-dark shadow-[0_8px_30px_rgba(240,168,50,0.4)] hover:-translate-y-0.5 hover:brightness-110 transition"
          >
            Begin Your Application →
          </Link>
        </div>
      </section>
    </>
  );
}
