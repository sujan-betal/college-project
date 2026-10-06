import ModulePage from "@/components/ModulePage";

export default function TeacherNotices() {
  return (
    <ModulePage
      title="Notices"
      desc="Post class-level notices and view institute announcements."
      stats={[{ n: "5", l: "POSTED" }, { n: "3", l: "THIS WEEK" }, { n: "118", l: "REACH" }, { n: "All", l: "ROLES" }]}
      columns={["Title", "Audience", "Posted", "Status"]}
      rows={[
        ["Lab 2 shifted to Friday", "CSE-3A", "03 Oct", "Live"],
        ["Mid-term prep session", "CSE-5B", "29 Sep", "Live"],
        ["Project topic approvals", "CSE-3A", "22 Sep", "Expired"],
      ]}
    />
  );
}
