import ModulePage from "@/components/ModulePage";

export default function AdminCourses() {
  return (
    <ModulePage
      title="Courses"
      desc="Programs offered, seat counts, and fee structures."
      stats={[{ n: "38", l: "PROGRAMS" }, { n: "6", l: "PG" }, { n: "2,400", l: "SEATS" }, { n: "87%", l: "FILLED" }]}
      columns={["Program", "Duration", "Seats", "Fee"]}
      rows={[
        ["B.Tech CSE & AI", "4 yrs", "120", "₹1.1L/yr"],
        ["B.Sc Data Science", "3 yrs", "60", "₹70k/yr"],
        ["MBA Analytics", "2 yrs", "40", "₹1.6L/yr"],
      ]}
    />
  );
}
