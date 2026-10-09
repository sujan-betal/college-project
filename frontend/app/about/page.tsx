"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import PageBanner from "@/components/PageBanner";

export default function About() {
  const [content, setContent] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.publicSiteContent().then((res) => {
      if (res.success) setContent(res.data || {});
      setLoading(false);
    });
  }, []);

  const cards = Object.entries(content).filter(([key]) => key !== "college_name" && key !== "slogan");

  return (
    <>
      <PageBanner
        kicker="OUR STORY"
        title={content.about_title || "About AstraVidya"}
        text={content.about || ""}
      />
      <section className="mx-auto grid max-w-6xl gap-8 px-4 py-14 md:grid-cols-3">
        {loading ? (
          <p className="text-sm text-ink/50">Loading...</p>
        ) : cards.length === 0 ? (
          <p className="text-sm text-ink/50">No content available yet.</p>
        ) : (
          cards.map(([key, value]) => (
            <div key={key} className="rounded-2xl border border-ink/10 bg-white p-6 shadow-sm">
              <h2 className="font-display text-2xl font-bold text-maroon capitalize">{key.replace(/_/g, " ")}</h2>
              <p className="mt-2 text-ink/70">{value}</p>
            </div>
          ))
        )}
      </section>
    </>
  );
}