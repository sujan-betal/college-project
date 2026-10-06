import ModulePage from "@/components/ModulePage";

export default function AdminAdmissions() {
  return (
    <ModulePage
      title="Admissions"
      desc="Applications queue — review, approve, or reject."
      stats={[{ n: "312", l: "APPLIED" }, { n: "42", l: "PENDING" }, { n: "198", l: "APPROVED" }, { n: "72", l: "REJECTED" }]}
      columns={["Applicant", "Program", "Applied On", "Status"]}
      rows={[
        ["Ananya Sen", "B.Tech CSE", "02 Oct", "Pending"],
        ["Rohan Mallick", "BBA", "28 Sep", "Approved"],
        ["Tara Khan", "B.Sc DS", "25 Sep", "Rejected"],
      ]}
    />
  );
}
