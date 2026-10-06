import ModulePage from "@/components/ModulePage";

export default function AdminTeachers() {
  return (
    <ModulePage
      title="Teachers"
      desc="Faculty directory with subjects and extra permissions."
      stats={[{ n: "226", l: "TOTAL" }, { n: "34", l: "HOD ROLES" }, { n: "6", l: "NOTICE RIGHTS" }, { n: "8", l: "ON LEAVE" }]}
      columns={["Name", "Department", "Subjects", "Extra Rights"]}
      rows={[
        ["Dr. Meera Iyer", "CSE", "ML, NLP", "Notice posting"],
        ["Prof. Vikram Rao", "Mech", "Thermal, Design", "Leave approval"],
        ["Dr. Sana Qureshi", "Data Science", "Statistics", "—"],
      ]}
    />
  );
}
