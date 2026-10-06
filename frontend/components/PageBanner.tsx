export default function PageBanner({
  title,
  kicker,
  text,
}: {
  title: string;
  kicker: string;
  text: string;
}) {
  return (
    <section className="bg-gradient-to-r from-maroon-dark via-maroon to-maroon-dark text-white">
      <div className="mx-auto max-w-6xl px-4 py-10 md:py-16">
        <p className="inline-block rounded-full bg-saffron px-4 py-1 text-xs font-bold tracking-[0.3em] text-maroon-dark">{kicker}</p>
        <h1 className="mt-3 font-display text-3xl font-black text-white md:text-5xl">
          {title}
        </h1>
        <p className="mt-4 max-w-2xl text-white/90">{text}</p>
      </div>
    </section>
  );
}
