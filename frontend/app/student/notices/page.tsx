import ModulePage from "@/components/ModulePage";

export default function StudentNotices() {
  return (
    <ModulePage
      title="Notices"
      desc="Announcements from the institute and your faculty."
      stats={[{ n: "12", l: "ACTIVE" }, { n: "4", l: "THIS WEEK" }, { n: "2", l: "IMPORTANT" }, { n: "All", l: "ROLES" }]}
      columns={["Title", "From", "Posted", "Status"]}
      rows={[
        ["Exam schedule out", "Admin", "28 Sep", "Live"],
        ["Lab 2 shifted to Friday", "Prof. Ghosh", "03 Oct", "Live"],
        ["Scholarship deadline", "Admin", "25 Sep", "Live"],
      ]}
    />
  );
}
