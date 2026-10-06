import ModulePage from "@/components/ModulePage";

export default function StudentCertificates() {
  return (
    <ModulePage
      title="Certificates"
      desc="Request and download bonafide, character certificates, and more."
      stats={[{ n: "2", l: "ISSUED" }, { n: "1", l: "PENDING" }, { n: "3", l: "REQUESTS" }, { n: "2 days", l: "AVG TURN" }]}
      columns={["Type", "Requested", "Status", "Download"]}
      rows={[
        ["Bonafide", "01 Oct", "Issued", "PDF"],
        ["Character certificate", "28 Sep", "Pending", "—"],
        ["Fee structure letter", "20 Sep", "Issued", "PDF"],
      ]}
    />
  );
}
