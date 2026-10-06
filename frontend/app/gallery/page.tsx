import PageBanner from "@/components/PageBanner";

const tiles = [
  "from-maroon to-maroon-dark",
  "from-teal to-ink",
  "from-saffron to-maroon",
  "from-ink to-maroon-dark",
  "from-maroon-dark to-teal",
  "from-teal to-maroon",
];

export default function Gallery() {
  return (
    <>
      <PageBanner kicker="CAMPUS LIFE" title="Gallery" text="A glimpse of our labs, fests, and the everyday life at AstraVidya." />
      <section className="mx-auto grid max-w-6xl grid-cols-2 gap-4 px-4 py-14 md:grid-cols-3">
        {tiles.map((t, i) => (
          <div
            key={i}
            className={`h-44 rounded-2xl bg-gradient-to-br ${t} grid place-items-center text-cream/70 font-display text-lg hover:scale-[1.02] transition`}
          >
            Photo {i + 1}
          </div>
        ))}
      </section>
    </>
  );
}
