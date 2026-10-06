import ModulePage from "@/components/ModulePage";

export default function AuditLogs() {
  return (
    <ModulePage
      title="Audit Logs"
      desc="Every sensitive change — who did what, and when."
      stats={[{ n: "1,204", l: "ENTRIES" }, { n: "38", l: "TODAY" }, { n: "6", l: "CRITICAL" }, { n: "180d", l: "RETAINED" }]}
      columns={["When", "User", "Action", "Target"]}
      rows={[
        ["06 Oct 10:12", "super_admin", "permissions.update", "user:priya"],
        ["06 Oct 09:40", "rahul", "student.create", "AV2026-1042"],
        ["05 Oct 17:05", "neha", "notice.publish", "exam-schedule"],
        ["05 Oct 15:32", "super_admin", "subadmin.deactivate", "user:amit"],
      ]}
    />
  );
}
