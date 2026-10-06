import PageBanner from "@/components/PageBanner";

const notices = [
  ["05 Oct", "Scholarship applications close 20 October."],
  ["28 Sep", "Semester exams begin 8 January — schedule published."],
  ["15 Sep", "TechFest 2026 registrations open."],
  ["02 Sep", "Hostel fee payment deadline extended to 30 September."],
  ["20 Aug", "New AI & ML lab inaugurated by the Director."],
];

export default function Notices() {
  return (
    <>
      <PageBanner kicker="ANNOUNCEMENTS" title="Notices & News" text="Official announcements for students, parents, and staff — updated daily." />
      <section className="mx-auto max-w-4xl px-4 py-14">
        <ul className="divide-y divide-ink/10 rounded-2xl border border-ink/10 bg-white">
          {notices.map(([date, text]) => (
            <li key={text} className="flex flex-col gap-2 px-4 py-4 sm:flex-row sm:items-center sm:gap-4 sm:px-6">
              <span className="w-fit rounded-full bg-saffron-soft px-3 py-1 text-xs font-bold text-maroon">{date}</span>
              <p>{text}</p>
            </li>
          ))}
        </ul>
      </section>
    </>
  );
}
