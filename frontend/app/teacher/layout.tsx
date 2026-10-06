import PortalShell from "@/components/PortalShell";

const links: [string, string][] = [
  ["Overview", "/teacher"],
  ["Attendance", "/teacher/attendance"],
  ["Marks", "/teacher/marks"],
  ["Materials", "/teacher/materials"],
  ["Assignments", "/teacher/assignments"],
  ["Notices", "/teacher/notices"],
  ["Leave", "/teacher/leave"],
  ["Timetable", "/teacher/timetable"],
];

export default function TeacherLayout({ children }: { children: React.ReactNode }) {
  return (
    <PortalShell brand="AstraVidya" role="TEACHER" links={links}>
      {children}
    </PortalShell>
  );
}
