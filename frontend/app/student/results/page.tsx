import ModulePage from "@/components/ModulePage";

export default function StudentResults() {
  return (
    <ModulePage
      title="Results"
      desc="Your exam results and semester performance."
      stats={[{ n: "8.1", l: "CGPA" }, { n: "3", l: "BACKLOGS" }, { n: "2", l: "EXAMS" }, { n: "Top 10%", l: "RANK" }]}
      columns={["Exam", "Semester", "Marks", "Grade"]}
      rows={[
        ["Mid-Term", "3", "214/250", "A"],
        ["Practical", "3", "96/100", "A+"],
        ["Semester End", "2", "—", "Upcoming"],
      ]}
    />
  );
}
