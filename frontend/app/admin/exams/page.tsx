import ModulePage from "@/components/ModulePage";

export default function AdminExams() {
  return (
    <ModulePage
      title="Exams"
      desc="Exam schedules, results publishing, and admit cards."
      stats={[{ n: "3", l: "UPCOMING" }, { n: "12", l: "PUBLISHED" }, { n: "1,980", l: "APPEARED" }, { n: "91%", l: "PASSED" }]}
      columns={["Exam", "Date", "Semester", "Status"]}
      rows={[
        ["Semester End", "08 Jan", "3", "Scheduled"],
        ["Mid-Term", "10 Oct", "5", "Results out"],
        ["Practical Viva", "12 Oct", "3", "Scheduled"],
      ]}
    />
  );
}
