import ModulePage from "@/components/ModulePage";

export default function StudentAssignments() {
  return (
    <ModulePage
      title="Assignments"
      desc="Your pending and submitted assignments."
      stats={[{ n: "3", l: "PENDING" }, { n: "12", l: "SUBMITTED" }, { n: "1", l: "OVERDUE" }, { n: "8.4", l: "AVG SCORE" }]}
      columns={["Title", "Subject", "Due", "Status"]}
      rows={[
        ["Chip fab report", "VLSI", "12 Oct", "Pending"],
        ["K-map worksheet", "Digital Logic", "10 Oct", "Submitted"],
        ["Graphs problem set", "Discrete Math", "05 Oct", "Overdue"],
      ]}
    />
  );
}
