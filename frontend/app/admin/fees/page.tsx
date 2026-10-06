import ModulePage from "@/components/ModulePage";

export default function AdminFees() {
  return (
    <ModulePage
      title="Fees"
      desc="Fee structures, collections, and due lists."
      stats={[{ n: "₹4.2Cr", l: "COLLECTED" }, { n: "₹38L", l: "DUE" }, { n: "61", l: "DEFAULTERS" }, { n: "94%", l: "ON TIME" }]}
      columns={["Student", "Program", "Due Date", "Balance"]}
      rows={[
        ["Aarav Sharma", "B.Tech CSE", "31 Oct", "₹22,000"],
        ["Diya Roy", "BBA", "15 Oct", "Paid"],
        ["Kabir Singh", "B.Tech Mech", "31 Oct", "₹45,000"],
      ]}
    />
  );
}
