import ModulePage from "@/components/ModulePage";

export default function SubAdmins() {
  return (
    <ModulePage
      title="Sub-Admins"
      desc="Create sub-admins and control exactly what each can manage."
      stats={[{ n: "9", l: "ACTIVE" }, { n: "2", l: "DISABLED" }, { n: "4", l: "TEMPLATES" }, { n: "31", l: "PERMISSIONS" }]}
      columns={["Name", "Email", "Template", "Status"]}
      rows={[
        ["Priya Sen", "priya@astravidya.edu", "Accountant", "Active"],
        ["Rahul Das", "rahul@astravidya.edu", "Admission Officer", "Active"],
        ["Neha Kapoor", "neha@astravidya.edu", "Content Manager", "Active"],
        ["Amit Jain", "amit@astravidya.edu", "Exam Controller", "Disabled"],
      ]}
    />
  );
}
