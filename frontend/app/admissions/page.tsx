import PageBanner from "@/components/PageBanner";

export default function Admissions() {
  return (
    <>
      <PageBanner
        kicker="JOIN US"
        title="Admissions 2026–27"
        text="Applications for under-graduate and post-graduate programs are open. Admissions are need-blind for merit seats and supported by scholarships."
      />
      <section className="mx-auto max-w-3xl px-4 py-14">
        <h2 className="font-display text-3xl font-bold text-maroon">Apply Online</h2>
        <form className="mt-6 space-y-4 rounded-2xl border border-ink/10 bg-white p-6 shadow-sm">
          <div className="grid gap-4 md:grid-cols-2">
            <input required placeholder="Full name" className="rounded-lg border border-ink/15 px-4 py-2.5" />
            <input required type="email" placeholder="Email" className="rounded-lg border border-ink/15 px-4 py-2.5" />
            <input required placeholder="Phone" className="rounded-lg border border-ink/15 px-4 py-2.5" />
            <input required placeholder="Program of interest" className="rounded-lg border border-ink/15 px-4 py-2.5" />
          </div>
          <textarea rows={4} placeholder="Tell us about yourself" className="w-full rounded-lg border border-ink/15 px-4 py-2.5" />
          <button className="rounded-full bg-maroon px-8 py-3 font-semibold text-cream hover:bg-maroon-dark transition">
            Submit Application
          </button>
          <p className="text-xs text-ink/50">This is a design preview — submissions are not yet connected to a backend.</p>
        </form>
      </section>
    </>
  );
}
