import Link from "next/link";

const links = [
  ["About", "/about"],
  ["Courses", "/courses"],
  ["Admissions", "/admissions"],
  ["Departments", "/departments"],
  ["Faculty", "/faculty"],
  ["Notices", "/notices"],
  ["Gallery", "/gallery"],
  ["Events", "/events"],
  ["Contact", "/contact"],
];

export default function Header() {
  return (
    <header className="sticky top-0 z-50 bg-maroon text-cream shadow-lg">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link href="/" className="flex items-center gap-3">
          <span className="grid h-10 w-10 place-items-center rounded-full bg-saffron font-display text-xl font-black text-maroon-dark">
            A
          </span>
          <span className="font-display text-lg font-bold leading-tight">
            AstraVidya
            <span className="block text-[10px] font-normal tracking-[0.3em] text-saffron-soft">
              INSTITUTE OF TECHNOLOGY
            </span>
          </span>
        </Link>
        <Link
          href="/login"
          className="rounded-full border border-saffron px-4 py-1.5 text-sm font-semibold text-saffron hover:bg-saffron hover:text-maroon-dark transition"
        >
          Portal Login
        </Link>
      </div>
      <nav className="border-t border-white/10 bg-maroon-dark">
        <ul className="mx-auto flex max-w-6xl gap-x-5 gap-y-1 overflow-x-auto whitespace-nowrap px-4 py-2 text-sm md:flex-wrap">
          {links.map(([label, href]) => (
            <li key={href}>
              <Link href={href} className="hover:text-saffron transition">
                {label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
}
