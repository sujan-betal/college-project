"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";

export default function ChangePassword() {
  const router = useRouter();
  const [current_password, setCurrent] = useState("");
  const [new_password, setNew] = useState("");
  const [confirm_password, setConfirm] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setMessage("");
    if (new_password !== confirm_password) {
      setError("Passwords do not match");
      return;
    }
    setLoading(true);
    const res = await api.changePassword(current_password, new_password, confirm_password);
    setLoading(false);
    if (!res.success) {
      setError(res.message || "Failed to change password");
      return;
    }
    setMessage("Password changed. Redirecting...");
    setTimeout(() => {
      const role = (localStorage.getItem("role") || "").toUpperCase();
      if (role === "ADMIN") router.replace("/admin");
      else if (role === "TEACHER") router.replace("/teacher");
      else router.replace("/student");
    }, 800);
  }

  return (
    <section className="grain bg-maroon text-cream">
      <div className="mx-auto flex min-h-[70vh] max-w-md flex-col justify-center px-4 py-16">
        <h1 className="font-display text-4xl font-black">Change Password</h1>
        <form onSubmit={handleSubmit} className="mt-8 space-y-4 rounded-2xl bg-cream p-6 text-ink shadow-xl">
          <input required type="password" placeholder="Current password" value={current_password} onChange={(e) => setCurrent(e.target.value)} className="w-full rounded-lg border border-ink/15 px-4 py-2.5" />
          <input required type="password" placeholder="New password (min 8)" value={new_password} onChange={(e) => setNew(e.target.value)} className="w-full rounded-lg border border-ink/15 px-4 py-2.5" />
          <input required type="password" placeholder="Confirm new password" value={confirm_password} onChange={(e) => setConfirm(e.target.value)} className="w-full rounded-lg border border-ink/15 px-4 py-2.5" />
          {error && <p className="text-sm text-red-600">{error}</p>}
          {message && <p className="text-sm text-green-700">{message}</p>}
          <button disabled={loading} className="w-full rounded-full bg-maroon py-3 font-semibold text-cream hover:bg-maroon-dark transition disabled:opacity-60">
            {loading ? "Updating..." : "Update Password"}
          </button>
        </form>
      </div>
    </section>
  );
}
