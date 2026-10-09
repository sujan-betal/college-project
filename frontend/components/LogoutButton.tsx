"use client";

import { clearSession } from "@/lib/api";
import { useRouter } from "next/navigation";

export default function LogoutButton() {
  const router = useRouter();
  return (
    <button
      onClick={() => {
        clearSession();
        router.replace("/login");
      }}
      className="mt-4 w-full rounded-lg border border-ink/15 px-3 py-2 text-sm hover:bg-saffron-soft hover:text-maroon transition"
    >
      Logout
    </button>
  );
}
