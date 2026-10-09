"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function TeacherMarks() {
  const [rows, setRows] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [form, setForm] = useState({ student_id: "", exam_id: "", subject_id: "", marks_obtained: "", marks_total: "" });

  function load() {
    setLoading(true);
    api.teacherMarks().then((res) => {
      if (res.success) setRows(res.data || []);
      setLoading(false);
    });
  }

  useEffect(load, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setMessage("");
    const res = await api.teacherAddMarks({
      student_id: Number(form.student_id),
      exam_id: Number(form.exam_id),
      subject_id: Number(form.subject_id),
      marks_obtained: Number(form.marks_obtained),
      marks_total: Number(form.marks_total),
    });
    if (res.success) {
      setMessage("Marks added.");
      setForm({ student_id: "", exam_id: "", subject_id: "", marks_obtained: "", marks_total: "" });
      load();
    } else {
      setMessage(res.message || "Failed to add marks");
    }
  }

  const columns = rows.length > 0 ? Object.keys(rows[0]).slice(0, 6) : [];

  return (
    <>
      <h1 className="font-display text-3xl font-black text-maroon">Marks</h1>
      <p className="mt-1 text-ink/80">Enter marks for exams in your assigned subjects only.</p>
      <form onSubmit={handleSubmit} className="mt-6 grid gap-3 rounded-2xl border border-ink/10 bg-white p-6 shadow-sm md:grid-cols-3">
        <input required placeholder="Student ID" type="number" value={form.student_id} onChange={(e) => setForm({ ...form, student_id: e.target.value })} className="rounded-lg border border-ink/15 px-4 py-2.5" />
        <input required placeholder="Exam ID" type="number" value={form.exam_id} onChange={(e) => setForm({ ...form, exam_id: e.target.value })} className="rounded-lg border border-ink/15 px-4 py-2.5" />
        <input required placeholder="Subject ID" type="number" value={form.subject_id} onChange={(e) => setForm({ ...form, subject_id: e.target.value })} className="rounded-lg border border-ink/15 px-4 py-2.5" />
        <input required placeholder="Marks obtained" type="number" value={form.marks_obtained} onChange={(e) => setForm({ ...form, marks_obtained: e.target.value })} className="rounded-lg border border-ink/15 px-4 py-2.5" />
        <input required placeholder="Marks total" type="number" value={form.marks_total} onChange={(e) => setForm({ ...form, marks_total: e.target.value })} className="rounded-lg border border-ink/15 px-4 py-2.5" />
        <button className="rounded-full bg-maroon px-6 py-2.5 font-semibold text-cream">Add Marks</button>
      </form>
      {message && <p className="mt-2 text-sm text-ink/70">{message}</p>}
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
              <tr><td className="px-4 py-3">No marks records.</td></tr>
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
