import PageBanner from "@/components/PageBanner";

export default function About() {
  return (
    <>
      <PageBanner
        kicker="OUR STORY"
        title="About AstraVidya"
        text="Founded in 1998, we have grown from a single engineering wing to a full university-grade institute serving 4,200+ students across 38 programs."
      />
      <section className="mx-auto grid max-w-6xl gap-8 px-4 py-14 md:grid-cols-3">
        {[
          ["Vision", "To be a centre of excellence where learning, research, and industry meet."],
          ["Mission", "Affordable quality education, strong ethics, and careers that matter."],
          ["Values", "Curiosity, integrity, inclusion, and relentless improvement."],
        ].map(([t, d]) => (
          <div key={t} className="rounded-2xl border border-ink/10 bg-white p-6 shadow-sm">
            <h2 className="font-display text-2xl font-bold text-maroon">{t}</h2>
            <p className="mt-2 text-ink/70">{d}</p>
          </div>
        ))}
      </section>
      <section className="mx-auto max-w-6xl px-4 pb-16">
        <h2 className="font-display text-3xl font-bold">Milestones</h2>
        <ol className="mt-6 border-l-2 border-saffron pl-6 space-y-6">
          {[
            ["1998", "Founded with 3 departments and 120 students."],
            ["2009", "NAAC A grade accreditation."],
            ["2017", "Upgraded to A++ with 100% placement drive in 5 core sectors."],
            ["2024", "Ranked among top 150 engineering colleges in India."],
          ].map(([y, d]) => (
            <li key={y}>
              <p className="font-display font-bold text-maroon">{y}</p>
              <p className="text-ink/70">{d}</p>
            </li>
          ))}
        </ol>
      </section>
    </>
  );
}
