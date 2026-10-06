import ModulePage from "@/components/ModulePage";

export default function TeacherAssignments() {
  return (
    <ModulePage
      title="Assignments"
      desc="Create assignments and review submissions from your students."
      stats={[{ n: "7", l: "ACTIVE" }, { n: "142", l: "SUBMISSIONS" }, { n: "19", l: "TO GRADE" }, { n: "2", l: "OVERDUE" }]}
      columns={["Title", "Due", "Submitted", "Status"]}
      rows={[
        ["Chip fabrication report", "12 Oct", "54/60", "Open"],
        ["NLP mini-project", "10 Oct", "41/60", "Grading"],
        ["Unit 2 worksheet", "28 Sep", "60/60", "Closed"],
      ]}
    />
  );
}
