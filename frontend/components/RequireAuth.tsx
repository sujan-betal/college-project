"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { getAccessToken, getRole } from "@/lib/api";

const roleHome: Record<string, string> = {
  ADMIN: "/admin",
  TEACHER: "/teacher",
  STUDENT: "/student",
};

export default function RequireAuth({
  role,
  children,
}: {
  role: string;
  children: React.ReactNode;
}) {
  const router = useRouter();

  useEffect(() => {
    const token = getAccessToken();
    const userRole = (getRole() || "").toUpperCase();

    if (!token) {
      router.replace("/login");
      return;
    }

    if (userRole !== role) {
      router.replace(roleHome[userRole] || "/login");
    }
  }, [role, router]);

  return <>{children}</>;
}