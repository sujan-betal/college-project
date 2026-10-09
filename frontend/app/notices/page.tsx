"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import PageBanner from "@/components/PageBanner";

export default function Notices() {
  const [rows, setRows] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.publicNotices().then((res) => {
      if (res.success) setRows(res.data || []);
      setLoading(false);
    });
  }, []);

  return (
    <>
      <PageBanner kicker="ANNOUNCEMENTS" title="Notices & News" text="Official announcements for students, parents, and staff — updated daily." />
      <section className="mx-auto max-w-4xl px-4 py-14">
        {loading ? (
          <p className="text-sm text-ink/50">Loading notices...</p>
        ) : rows.length === 0 ? (
          <p className="text-sm text-ink/50">No notices published.</p>
        ) : (
          <ul className="divide-y divide-ink/10 rounded-2xl border border-ink/10 bg-white">
            {rows.map((n) => (
              <li key={n.id} className="flex flex-col gap-2 px-4 py-4 sm:flex-row sm:items-center sm:gap-4 sm:px-6">
                <span className="w-fit rounded-full bg-saffron-soft px-3 py-1 text-xs font-bold text-maroon">
                  {n.created_at ? new Date(n.created_at).toLocaleDateString() : "-"}
                </span>
                <div>
                  <p className="font-semibold">{n.title}</p>
                  <p className="text-sm text-ink/60">{n.body}</p>
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>
    </>
  );
}