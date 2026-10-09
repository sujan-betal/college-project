"use client";

import { useEffect, useState } from "react";
import { api, getUsername } from "@/lib/api";

export default function TeacherOverview() {
  const [profile, setProfile] = useState<any>(null);
  const [subjects, setSubjects] = useState<any[]>([]);

  useEffect(() => {
    api.teacherProfile().then((res) => res.success && setProfile(res.data));
    api.teacherSubjects().then((res) => res.success && setSubjects(res.data || []));
  }, []);

  return (
    <>
      <h1 className="font-display text-3xl font-black text-maroon">Welcome, {getUsername() || "Teacher"}</h1>
      <p className="mt-1 text-ink/60">
        {profile ? `${profile.designation} · Employee ${profile.employee_id}` : "Loading your profile..."}
      </p>
      <div className="mt-6 grid grid-cols-2 gap-4 md:grid-cols-4">
        <div className="rounded-2xl border border-ink/10 bg-white p-5 shadow-sm">
          <p className="font-display text-3xl font-black text-maroon">{subjects.length}</p>
          <p className="text-xs tracking-widest text-ink/50">SUBJECTS</p>
        </div>
        <div className="rounded-2xl border border-ink/10 bg-white p-5 shadow-sm">
          <p className="font-display text-3xl font-black text-maroon">{profile?.department_id ?? "-"}</p>
          <p className="text-xs tracking-widest text-ink/50">DEPT ID</p>
        </div>
        <div className="rounded-2xl border border-ink/10 bg-white p-5 shadow-sm">
          <p className="font-display text-3xl font-black text-maroon">{profile?.is_department_head ? "Yes" : "No"}</p>
          <p className="text-xs tracking-widest text-ink/50">DEPT HEAD</p>
        </div>
      </div>
      <h2 className="mt-10 font-display text-xl font-bold">Your Subjects</h2>
      <ul className="mt-4 space-y-3">
        {subjects.length === 0 ? (
          <li className="rounded-xl border border-ink/10 bg-white px-4 py-3 text-sm">No subjects assigned.</li>
        ) : subjects.map((s, i) => (
          <li key={i} className="rounded-xl border border-ink/10 bg-white px-4 py-3 text-sm">
            Subject {s.subject_id} · Course {s.course_id} · Section {s.section} · {s.academic_year}
          </li>
        ))}
      </ul>
    </>
  );
}
