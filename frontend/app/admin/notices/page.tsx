import ModulePage from "@/components/ModulePage";

export default function AdminNotices() {
  return (
    <ModulePage
      title="Notices"
      desc="Post targeted announcements to students, teachers, or everyone."
      stats={[{ n: "18", l: "ACTIVE" }, { n: "5", l: "THIS WEEK" }, { n: "3", l: "TARGETED" }, { n: "All", l: "ROLES" }]}
      columns={["Title", "Audience", "Posted", "Status"]}
      rows={[
        ["Exam schedule out", "All", "28 Sep", "Live"],
        ["Library timing change", "Students", "21 Sep", "Live"],
        ["Faculty meet Friday", "Teachers", "19 Sep", "Live"],
      ]}
    />
  );
}
