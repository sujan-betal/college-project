"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function AdminFees() {
  const [rows, setRows] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [form, setForm] = useState({ course_id: "", head: "", amount: "", due_date: "" });

  function load() {
    setLoading(true);
    api.adminFees().then((res) => {
      if (res.success) setRows(res.data || []);
      setLoading(false);
    });
  }

  useEffect(load, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setMessage("");
    const res = await api.adminCreateFee({
      course_id: Number(form.course_id),
      head: form.head,
      amount: Number(form.amount),
      due_date: form.due_date || undefined,
    });
    if (res.success) {
      setMessage("Fee created.");
      setForm({ course_id: "", head: "", amount: "", due_date: "" });
      load();
    } else {
      setMessage(res.message || "Failed to create fee");
    }
  }

  return (
    <>
      <h1 className="font-display text-3xl font-black text-maroon">Fees</h1>
      <p className="mt-1 text-ink/80">Fee structure, collections, and dues tracking.</p>
      <form onSubmit={handleSubmit} className="mt-6 grid gap-3 rounded-2xl border border-ink/10 bg-white p-6 shadow-sm md:grid-cols-4">
        <input required placeholder="Course ID" type="number" value={form.course_id} onChange={(e) => setForm({ ...form, course_id: e.target.value })} className="rounded-lg border border-ink/15 px-4 py-2.5" />
        <input required placeholder="Head" value={form.head} onChange={(e) => setForm({ ...form, head: e.target.value })} className="rounded-lg border border-ink/15 px-4 py-2.5" />
        <input required placeholder="Amount" type="number" value={form.amount} onChange={(e) => setForm({ ...form, amount: e.target.value })} className="rounded-lg border border-ink/15 px-4 py-2.5" />
        <input placeholder="Due date" type="date" value={form.due_date} onChange={(e) => setForm({ ...form, due_date: e.target.value })} className="rounded-lg border border-ink/15 px-4 py-2.5" />
        <button className="rounded-full bg-maroon px-6 py-2.5 font-semibold text-cream md:col-span-4 w-fit">Create Fee</button>
      </form>
      {message && <p className="mt-2 text-sm text-ink/70">{message}</p>}
      <div className="mt-8 overflow-x-auto rounded-2xl border border-ink/10 bg-white shadow-sm">
        <table className="w-full min-w-[560px] text-sm">
          <thead>
            <tr className="bg-maroon text-cream">
              <th className="px-4 py-3 text-left font-semibold">Course</th>
              <th className="px-4 py-3 text-left font-semibold">Head</th>
              <th className="px-4 py-3 text-left font-semibold">Amount</th>
              <th className="px-4 py-3 text-left font-semibold">Due</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={4} className="px-4 py-3">Loading...</td></tr>
            ) : rows.length === 0 ? (
              <tr><td colSpan={4} className="px-4 py-3">No fee records.</td></tr>
            ) : rows.map((r, i) => (
              <tr key={r.id ?? i} className={i % 2 ? "bg-cream/60" : ""}>
                <td className="px-4 py-3">{r.course_id}</td>
                <td className="px-4 py-3">{r.head}</td>
                <td className="px-4 py-3">{r.amount}</td>
                <td className="px-4 py-3">{r.due_date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
