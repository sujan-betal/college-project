import PortalShell from "@/components/PortalShell";

const links: [string, string][] = [
  ["Overview", "/student"],
  ["Attendance", "/student/attendance"],
  ["Results", "/student/results"],
  ["Fees", "/student/fees"],
  ["Materials", "/student/materials"],
  ["Assignments", "/student/assignments"],
  ["Notices", "/student/notices"],
  ["Certificates", "/student/certificates"],
];

export default function StudentLayout({ children }: { children: React.ReactNode }) {
  return (
    <PortalShell brand="AstraVidya" role="STUDENT" links={links}>
      {children}
    </PortalShell>
  );
}
