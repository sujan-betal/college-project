import ModulePage from "@/components/ModulePage";

export default function TeacherMarks() {
  return (
    <ModulePage
      title="Marks"
      desc="Enter marks for exams in your assigned subjects only."
      stats={[{ n: "2", l: "EXAMS" }, { n: "118", l: "STUDENTS" }, { n: "76%", l: "ENTERED" }, { n: "8.1", l: "CLASS AVG" }]}
      columns={["Student", "Mid-Term", "Practical", "Total"]}
      rows={[
        ["Aarav Sharma", "18/25", "19/25", "37/50"],
        ["Isha Patel", "12/25", "15/25", "27/50"],
        ["Rohan Mehta", "21/25", "20/25", "41/50"],
      ]}
    />
  );
}
