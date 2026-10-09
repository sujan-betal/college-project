"use client";

import { useState } from "react";
import { api } from "@/lib/api";

export default function TeacherNotices() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [audience, setAudience] = useState("STUDENT");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setMessage("");
    const res = await api.teacherPostNotice({ title, content, audience });
    setLoading(false);
    if (res.success) {
      setMessage("Notice posted.");
      setTitle("");
      setContent("");
    } else {
      setMessage(res.message || "Failed to post notice");
    }
  }

  return (
    <>
      <h1 className="font-display text-3xl font-black text-maroon">Notices</h1>
      <p className="mt-1 text-ink/80">Post class-level notices and institute announcements.</p>
      <form onSubmit={handleSubmit} className="mt-6 space-y-4 rounded-2xl border border-ink/10 bg-white p-6 shadow-sm">
        <input required placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} className="w-full rounded-lg border border-ink/15 px-4 py-2.5" />
        <textarea required placeholder="Content" rows={4} value={content} onChange={(e) => setContent(e.target.value)} className="w-full rounded-lg border border-ink/15 px-4 py-2.5" />
        <select value={audience} onChange={(e) => setAudience(e.target.value)} className="rounded-lg border border-ink/15 px-3 py-2">
          <option value="STUDENT">Students</option>
          <option value="TEACHER">Teachers</option>
          <option value="ALL">Everyone</option>
        </select>
        <button disabled={loading} className="rounded-full bg-maroon px-6 py-2.5 font-semibold text-cream disabled:opacity-60">
          {loading ? "Posting..." : "Post Notice"}
        </button>
        {message && <p className="text-sm text-ink/70">{message}</p>}
      </form>
    </>
  );
}
