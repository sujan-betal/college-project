"use client";

import Link from "next/link";
import { ReactNode, useEffect, useState } from "react";
import LogoutButton from "@/components/LogoutButton";
import { api, hasPermission } from "@/lib/api";
import { usePermissionRefresh } from "@/components/RequirePermission";

const linkPermissions: Record<string, string> = {
  "/admin/students": "USER_VIEW",
  "/admin/teachers": "USER_VIEW",
  "/admin/subadmins": "USER_VIEW",
  "/admin/courses": "COURSE_VIEW",
  "/admin/admissions": "ADMISSION_VIEW",
  "/admin/fees": "FEE_VIEW",
  "/admin/exams": "EXAM_VIEW",
  "/admin/notices": "NOTICE_VIEW",
  "/admin/content": "CONTENT_VIEW",
  "/admin/leave": "LEAVE_VIEW",
  "/admin/reports": "REPORT_VIEW",
  "/admin/audit-logs": "AUDIT_VIEW",
};

export default function PortalShell({
  brand,
  role,
  links,
  children,
}: {
  brand: string;
  role: string;
  links: [string, string][];
  children: ReactNode;
}) {
  // Re-filter sidebar links when permissions refresh in the background.
  usePermissionRefresh();
  const [me, setMe] = useState<{ username?: string; email?: string } | null>(null);

  useEffect(() => {
    api.me().then((res) => {
      if (res.success) setMe(res.data);
    });
  }, []);

  const visible = links.filter(([label, href]) => {
    const permission = linkPermissions[href];
    if (!permission) return true;
    return hasPermission(permission);
  });

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 md:flex md:gap-8">
      <aside className="mb-6 md:mb-0 md:w-56 md:shrink-0">
        <p className="font-display text-xl font-bold text-maroon">{brand}</p>
        <p className="mb-1 text-[10px] tracking-[0.3em] text-ink/50">
          {role} PORTAL
        </p>
        {me?.username && (
          <p className="mb-3 truncate text-xs text-ink/60">
            {me.username}
            {me.email ? ` · ${me.email}` : ""}
          </p>
        )}
        <nav className="flex gap-2 overflow-x-auto md:flex-col md:gap-1">
          {visible.map(([label, href]) => (
            <Link
              key={href}
              href={href}
              className="whitespace-nowrap rounded-lg px-3 py-2 text-sm hover:bg-saffron-soft hover:text-maroon transition"
            >
              {label}
            </Link>
          ))}
        </nav>
        <LogoutButton />
      </aside>
      <div className="min-w-0 flex-1">{children}</div>
    </div>
  );
}