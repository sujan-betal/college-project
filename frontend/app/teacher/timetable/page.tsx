import ModulePage from "@/components/ModulePage";

export default function TeacherTimetable() {
  return (
    <ModulePage
      title="Timetable"
      desc="Your weekly class schedule."
      stats={[{ n: "14", l: "PERIODS/WK" }, { n: "4", l: "SUBJECTS" }, { n: "2", l: "LABS" }, { n: "3", l: "OFFICE HRS" }]}
      columns={["Day", "10:00", "12:30", "14:00"]}
      rows={[
        ["Mon", "VLSI CSE-3A", "NLP CSE-5B", "—"],
        ["Tue", "NLP CSE-5B", "—", "Office hours"],
        ["Wed", "VLSI Lab", "VLSI Lab", "—"],
        ["Thu", "Embedded CSE-3A", "—", "Office hours"],
        ["Fri", "—", "Signals CSE-3A", "—"],
      ]}
    />
  );
}
