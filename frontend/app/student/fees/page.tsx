import ModulePage from "@/components/ModulePage";

export default function StudentFees() {
  return (
    <ModulePage
      title="Fees"
      desc="Fee dues, payments, and receipts."
      stats={[{ n: "₹22k", l: "DUE" }, { n: "₹1.1L", l: "PAID" }, { n: "31 Oct", l: "DUE DATE" }, { n: "6", l: "RECEIPTS" }]}
      columns={["Head", "Amount", "Due Date", "Status"]}
      rows={[
        ["Tuition Sem 3", "₹55,000", "31 Oct", "Pending"],
        ["Hostel", "₹22,000", "30 Sep", "Paid"],
        ["Exam fee", "₹2,500", "15 Sep", "Paid"],
      ]}
    />
  );
}
