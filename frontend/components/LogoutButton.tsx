"use client";

import { api, clearSession } from "@/lib/api";
import { useRouter } from "next/navigation";

export default function LogoutButton() {
  const router = useRouter();

  async function handleLogout() {
    // Tell the backend first, but never block the user on a network failure.
    try {
      await api.logout();
    } catch {
      // ignored
    }
    clearSession();
    router.replace("/login");
  }

  return (
    <button
      onClick={handleLogout}
      className="mt-4 w-full rounded-lg border border-ink/15 px-3 py-2 text-sm hover:bg-saffron-soft hover:text-maroon transition"
    >
      Logout
    </button>
  );
}