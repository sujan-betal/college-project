import ModulePage from "@/components/ModulePage";

export default function AdminStudents() {
  return (
    <ModulePage
      title="Students"
      desc="All enrolled students with their department and current semester."
      stats={[{ n: "4,218", l: "TOTAL" }, { n: "1,120", l: "FIRST YEAR" }, { n: "96%", l: "ACTIVE" }, { n: "12", l: "SUSPENDED" }]}
      columns={["Name", "Roll No", "Program", "Semester"]}
      rows={[
        ["Aarav Sharma", "AV2026-0142", "B.Tech CSE", "3"],
        ["Diya Roy", "AV2025-0881", "BBA Finance", "5"],
        ["Kabir Singh", "AV2024-0237", "B.Tech Mech", "7"],
        ["Isha Patel", "AV2026-1042", "B.Sc Data Science", "1"],
      ]}
    />
  );
}
