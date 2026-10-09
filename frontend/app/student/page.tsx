"use client";

import { useEffect, useState } from "react";
import { api, getUsername } from "@/lib/api";

export default function StudentOverview() {
  const [profile, setProfile] = useState<any>(null);
  const [noticeCount, setNoticeCount] = useState(0);

  useEffect(() => {
    api.studentProfile().then((res) => res.success && setProfile(res.data));
    api.studentNotices().then((res) => res.success && setNoticeCount((res.data || []).length));
  }, []);

  return (
    <>
      <h1 className="font-display text-3xl font-black text-maroon">Hi, {getUsername() || "Student"}</h1>
      <p className="mt-1 text-ink/60">
        {profile
          ? `Semester ${profile.semester} · Section ${profile.section} · Roll ${profile.roll_no}`
          : "Loading your profile..."}
      </p>
      <div className="mt-6 grid grid-cols-2 gap-4 md:grid-cols-4">
        <div className="rounded-2xl border border-ink/10 bg-white p-5 shadow-sm">
          <p className="font-display text-3xl font-black text-maroon">{profile?.guardian_phone || "-"}</p>
          <p className="text-xs tracking-widest text-ink/50">GUARDIAN PHONE</p>
        </div>
        <div className="rounded-2xl border border-ink/10 bg-white p-5 shadow-sm">
          <p className="font-display text-3xl font-black text-maroon">{profile?.department_id ?? "-"}</p>
          <p className="text-xs tracking-widest text-ink/50">DEPT ID</p>
        </div>
        <div className="rounded-2xl border border-ink/10 bg-white p-5 shadow-sm">
          <p className="font-display text-3xl font-black text-maroon">{profile?.course_id ?? "-"}</p>
          <p className="text-xs tracking-widest text-ink/50">COURSE ID</p>
        </div>
        <div className="rounded-2xl border border-ink/10 bg-white p-5 shadow-sm">
          <p className="font-display text-3xl font-black text-maroon">{noticeCount}</p>
          <p className="text-xs tracking-widest text-ink/50">NOTICES</p>
        </div>
      </div>
    </>
  );
}
