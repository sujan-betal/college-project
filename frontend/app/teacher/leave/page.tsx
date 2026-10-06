import ModulePage from "@/components/ModulePage";

export default function TeacherLeave() {
  return (
    <ModulePage
      title="Leave"
      desc="Apply for leave and track approvals."
      stats={[{ n: "9", l: "USED" }, { n: "3", l: "PENDING" }, { n: "12", l: "BALANCE" }, { n: "1", l: "REJECTED" }]}
      columns={["Period", "Reason", "Applied", "Status"]}
      rows={[
        ["10–12 Oct", "Family event", "04 Oct", "Pending"],
        ["02–03 Sep", "Medical", "28 Aug", "Approved"],
        ["14 Aug", "Personal", "10 Aug", "Rejected"],
      ]}
    />
  );
}
