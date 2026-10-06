import ModulePage from "@/components/ModulePage";

export default function AdminReports() {
  return (
    <ModulePage
      title="Reports"
      desc="Export Excel and PDF reports for finance, academics, and admissions."
      stats={[{ n: "14", l: "TEMPLATES" }, { n: "8", l: "THIS MONTH" }, { n: "2", l: "SCHEDULED" }, { n: "Excel+PDF", l: "FORMATS" }]}
      columns={["Report", "Generated", "Size", "Format"]}
      rows={[
        ["Fee collection Sep", "30 Sep", "1.2 MB", "Excel"],
        ["Attendance overview", "28 Sep", "840 KB", "PDF"],
        ["Admissions funnel", "25 Sep", "620 KB", "Excel"],
      ]}
    />
  );
}
