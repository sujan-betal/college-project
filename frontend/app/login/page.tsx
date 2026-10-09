"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api, saveSession } from "@/lib/api";

export default function Login() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    const res = await api.login(username, password);
    setLoading(false);

    if (!res.success) {
      setError(res.message || "Login failed");
      return;
    }

    saveSession({
      access_token: res.data.access_token,
      refresh_token: res.data.refresh_token,
      role: res.data.role,
      username: res.data.username,
      permissions: res.data.permissions || [],
    });

    if (res.data.is_reset) {
      router.replace("/change-password");
      return;
    }

    const role = (res.data.role || "").toUpperCase();
    if (role === "ADMIN") router.replace("/admin");
    else if (role === "TEACHER") router.replace("/teacher");
    else router.replace("/student");
  }

  return (
    <section className="grain bg-maroon text-cream">
      <div className="mx-auto flex min-h-[70vh] max-w-md flex-col justify-center px-4 py-16">
        <h1 className="font-display text-4xl font-black">Portal Login</h1>
        <p className="mt-2 text-cream/80">
          One login for students, teachers, and administrators. Your role decides
          where you land.
        </p>
        <form onSubmit={handleSubmit} className="mt-8 space-y-4 rounded-2xl bg-cream p-6 text-ink shadow-xl">
          <input
            required
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Username or email"
            className="w-full rounded-lg border border-ink/15 px-4 py-2.5"
          />
          <input
            required
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            className="w-full rounded-lg border border-ink/15 px-4 py-2.5"
          />
          {error && <p className="text-sm text-red-600">{error}</p>}
          <button
            disabled={loading}
            className="w-full rounded-full bg-maroon py-3 font-semibold text-cream hover:bg-maroon-dark transition disabled:opacity-60"
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>
      </div>
    </section>
  );
}
