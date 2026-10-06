import ModulePage from "@/components/ModulePage";

export default function AdminLeave() {
  return (
    <ModulePage
      title="Leave Requests"
      desc="Approve or reject teacher leave applications."
      stats={[{ n: "8", l: "PENDING" }, { n: "21", l: "APPROVED" }, { n: "3", l: "REJECTED" }, { n: "6", l: "UPCOMING" }]}
      columns={["Teacher", "From", "To", "Status"]}
      rows={[
        ["Prof. Vikram Rao", "10 Oct", "12 Oct", "Pending"],
        ["Dr. Sana Qureshi", "15 Oct", "16 Oct", "Approved"],
        ["Prof. Rohan Dutta", "21 Oct", "22 Oct", "Rejected"],
      ]}
    />
  );
}
