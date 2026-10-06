import ModulePage from "@/components/ModulePage";

export default function StudentMaterials() {
  return (
    <ModulePage
      title="Materials"
      desc="Notes and resources uploaded by your faculty."
      stats={[{ n: "18", l: "FILES" }, { n: "5", l: "SUBJECTS" }, { n: "1.2 GB", l: "TOTAL" }, { n: "PDF", l: "MOST" }]}
      columns={["Title", "Subject", "Faculty", "Size"]}
      rows={[
        ["VLSI Unit 3 slides", "VLSI", "Prof. Ghosh", "8.4 MB"],
        ["Digital Logic notes", "Digital Logic", "Prof. Rao", "3.1 MB"],
        ["Math formula sheet", "Discrete Math", "Dr. Nair", "1.2 MB"],
      ]}
    />
  );
}
