import Link from "next/link";
import { ReactNode } from "react";

export default function PortalShell({
  brand,
  role,
  links,
  children,
}: {
  brand: string;
  role: string;
  links: [string, string][];
  children: ReactNode;
}) {
  return (
    <div className="mx-auto max-w-7xl px-4 py-8 md:flex md:gap-8">
      <aside className="mb-6 md:mb-0 md:w-56 md:shrink-0">
        <p className="font-display text-xl font-bold text-maroon">{brand}</p>
        <p className="mb-4 text-[10px] tracking-[0.3em] text-ink/50">
          {role} PORTAL
        </p>
        <nav className="flex gap-2 overflow-x-auto md:flex-col md:gap-1">
          {links.map(([label, href]) => (
            <Link
              key={href}
              href={href}
              className="whitespace-nowrap rounded-lg px-3 py-2 text-sm hover:bg-saffron-soft hover:text-maroon transition"
            >
              {label}
            </Link>
          ))}
        </nav>
      </aside>
      <div className="min-w-0 flex-1">{children}</div>
    </div>
  );
}
