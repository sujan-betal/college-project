import PortalShell from "@/components/PortalShell";

const links: [string, string][] = [
  ["Dashboard", "/admin"],
  ["Sub-Admins", "/admin/subadmins"],
  ["Students", "/admin/students"],
  ["Teachers", "/admin/teachers"],
  ["Courses", "/admin/courses"],
  ["Admissions", "/admin/admissions"],
  ["Fees", "/admin/fees"],
  ["Exams", "/admin/exams"],
  ["Notices", "/admin/notices"],
  ["Content", "/admin/content"],
  ["Leave", "/admin/leave"],
  ["Reports", "/admin/reports"],
  ["Audit Logs", "/admin/audit-logs"],
];

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <PortalShell brand="AstraVidya" role="ADMIN" links={links}>
      {children}
    </PortalShell>
  );
}
