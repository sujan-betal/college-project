"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function AdminDashboard() {
  const [stats, setStats] = useState<{ total_users: number; students: number; teachers: number } | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.adminStats().then((res) => {
      if (res.success) setStats(res.data);
      else setError(res.message || "Failed to load stats");
    });
  }, []);

  const cards = [
    { n: stats ? String(stats.total_users) : "-", l: "Total Users" },
    { n: stats ? String(stats.students) : "-", l: "Students" },
    { n: stats ? String(stats.teachers) : "-", l: "Teachers" },
  ];

  return (
    <>
      <h1 className="font-display text-3xl font-black text-maroon">Admin Dashboard</h1>
      <p className="mt-1 text-ink/60">Everything happening across the institute, today.</p>
      {error && <p className="mt-3 text-sm text-red-600">{error}</p>}
      <div className="mt-6 grid grid-cols-2 gap-4 md:grid-cols-4">
        {cards.map((s) => (
          <div key={s.l} className="rounded-2xl border border-ink/10 bg-white p-5 shadow-sm">
            <p className="font-display text-3xl font-black text-maroon">{s.n}</p>
            <p className="text-xs tracking-widest text-ink/50">{s.l}</p>
          </div>
        ))}
      </div>
    </>
  );
}
