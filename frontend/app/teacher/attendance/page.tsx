import ModulePage from "@/components/ModulePage";

export default function TeacherAttendance() {
  return (
    <ModulePage
      title="Attendance"
      desc="Take and review attendance for your assigned subjects and sections."
      stats={[{ n: "3", l: "SECTIONS" }, { n: "118", l: "STUDENTS" }, { n: "92%", l: "AVG" }, { n: "6", l: "DETAIN RISK" }]}
      columns={["Student", "Roll No", "Present/Total", "%"]}
      rows={[
        ["Aarav Sharma", "AV2026-0142", "24/26", "92%"],
        ["Isha Patel", "AV2026-1042", "18/26", "69%"],
        ["Rohan Mehta", "AV2026-0198", "25/26", "96%"],
      ]}
    />
  );
}
