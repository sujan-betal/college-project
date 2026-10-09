"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function TeacherAttendance() {
  const [rows, setRows] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.teacherAttendance().then((res) => {
      if (res.success) setRows(res.data || []);
      setLoading(false);
    });
  }, []);

  const columns = rows.length > 0 ? Object.keys(rows[0]).slice(0, 5) : [];

  return (
    <>
      <h1 className="font-display text-3xl font-black text-maroon">Attendance</h1>
      <p className="mt-1 text-ink/80">Attendance records you have marked.</p>
      <div className="mt-8 overflow-x-auto rounded-2xl border border-ink/10 bg-white shadow-sm">
        <table className="w-full min-w-[560px] text-sm">
          <thead>
            <tr className="bg-maroon text-cream">
              {columns.map((c) => (
                <th key={c} className="px-4 py-3 text-left font-semibold">{c}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td className="px-4 py-3">Loading...</td></tr>
            ) : rows.length === 0 ? (
              <tr><td className="px-4 py-3">No attendance records.</td></tr>
            ) : rows.map((r, i) => (
              <tr key={r.id ?? i} className={i % 2 ? "bg-cream/60" : ""}>
                {columns.map((c) => (
                  <td key={c} className="px-4 py-3">{typeof r[c] === "object" ? JSON.stringify(r[c]) : String(r[c] ?? "-")}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
