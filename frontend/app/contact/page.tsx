import PageBanner from "@/components/PageBanner";

export default function Contact() {
  return (
    <>
      <PageBanner kicker="REACH US" title="Contact" text="Questions about admissions, fees, or campus visits? We usually reply within one working day." />
      <section className="mx-auto grid max-w-6xl gap-8 px-4 py-14 md:grid-cols-2">
        <div className="rounded-2xl border border-ink/10 bg-white p-6 shadow-sm">
          <h2 className="font-display text-2xl font-bold text-maroon">Send a message</h2>
          <form className="mt-4 space-y-4">
            <input required placeholder="Your name" className="w-full rounded-lg border border-ink/15 px-4 py-2.5" />
            <input required type="email" placeholder="Email" className="w-full rounded-lg border border-ink/15 px-4 py-2.5" />
            <textarea rows={5} placeholder="Message" className="w-full rounded-lg border border-ink/15 px-4 py-2.5" />
            <button className="rounded-full bg-maroon px-8 py-3 font-semibold text-cream hover:bg-maroon-dark transition">Send</button>
          </form>
        </div>
        <div className="space-y-4">
          <div className="rounded-2xl border border-ink/10 bg-white p-6">
            <h3 className="font-semibold">Address</h3>
            <p className="mt-1 text-ink/70">12 Knowledge Park, Sector 5, Kolkata, WB 700091</p>
          </div>
          <div className="rounded-2xl border border-ink/10 bg-white p-6">
            <h3 className="font-semibold">Phone & Email</h3>
            <p className="mt-1 text-ink/70">+91 33 4000 9000 · info@astravidya.edu</p>
          </div>
          <div className="h-56 rounded-2xl bg-gradient-to-br from-teal to-maroon grid place-items-center text-cream/70">
            Map preview
          </div>
        </div>
      </section>
    </>
  );
}
