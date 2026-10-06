import ModulePage from "@/components/ModulePage";

export default function StudentAttendance() {
  return (
    <ModulePage
      title="Attendance"
      desc="Your attendance across all subjects this semester."
      stats={[{ n: "91%", l: "OVERALL" }, { n: "5", l: "SUBJECTS" }, { n: "132/145", l: "PRESENT" }, { n: "1", l: "LOW SUBJ." }]}
      columns={["Subject", "Faculty", "Present/Total", "%"]}
      rows={[
        ["VLSI", "Prof. Ghosh", "24/26", "92%"],
        ["NLP", "Dr. Iyer", "22/26", "85%"],
        ["Digital Logic", "Prof. Rao", "25/28", "89%"],
        ["Discrete Math", "Dr. Nair", "18/24", "75%"],
      ]}
    />
  );
}
