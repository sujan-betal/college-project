import ModulePage from "@/components/ModulePage";

export default function TeacherMaterials() {
  return (
    <ModulePage
      title="Study Materials"
      desc="Upload notes, slides, and references for your classes."
      stats={[{ n: "24", l: "FILES" }, { n: "1.8k", l: "DOWNLOADS" }, { n: "6", l: "SUBJECTS" }, { n: "PDF", l: "MOST USED" }]}
      columns={["Title", "Subject", "Uploaded", "Downloads"]}
      rows={[
        ["VLSI — Unit 3 slides", "VLSI", "01 Oct", "312"],
        ["NLP — lecture notes", "NLP", "28 Sep", "187"],
        ["Lab manual v2", "VLSI", "20 Sep", "540"],
      ]}
    />
  );
}
