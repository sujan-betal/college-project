import ModulePage from "@/components/ModulePage";

export default function AdminContent() {
  return (
    <ModulePage
      title="Website Content"
      desc="Edit public pages, gallery, events, and home highlights."
      stats={[{ n: "10", l: "PAGES" }, { n: "6", l: "GALLERY" }, { n: "4", l: "EVENTS" }, { n: "4", l: "HIGHLIGHTS" }]}
      columns={["Section", "Last Edited", "By", "Status"]}
      rows={[
        ["Homepage hero", "02 Oct", "Neha Kapoor", "Published"],
        ["Gallery album", "30 Sep", "Neha Kapoor", "Published"],
        ["Events list", "28 Sep", "Admin", "Draft"],
      ]}
    />
  );
}
