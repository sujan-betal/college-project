import Link from "next/link";

export default function Footer() {
  return (
    <footer className="mt-16 bg-ink text-cream/80">
      <div className="mx-auto grid max-w-6xl gap-8 px-4 py-10 md:grid-cols-3">
        <div>
          <h3 className="font-display text-xl font-bold text-saffron">
            AstraVidya
          </h3>
          <p className="mt-2 text-sm">
            Igniting minds since 1998. NAAC A++ accredited. 85% placement
            record across 60+ companies.
          </p>
        </div>
        <div>
          <h4 className="font-semibold text-cream">Explore</h4>
          <ul className="mt-2 space-y-1 text-sm">
            <li><Link href="/courses" className="hover:text-saffron">Courses</Link></li>
            <li><Link href="/admissions" className="hover:text-saffron">Admissions</Link></li>
            <li><Link href="/notices" className="hover:text-saffron">Notices</Link></li>
            <li><Link href="/contact" className="hover:text-saffron">Contact</Link></li>
          </ul>
        </div>
        <div>
          <h4 className="font-semibold text-cream">Reach Us</h4>
          <p className="mt-2 text-sm">
            12 Knowledge Park, Sector 5<br />
            Kolkata, West Bengal 700091<br />
            +91 33 4000 9000<br />
            info@astravidya.edu
          </p>
        </div>
      </div>
      <p className="border-t border-white/10 py-4 text-center text-xs">
        © 2026 AstraVidya Institute of Technology. All rights reserved.
      </p>
    </footer>
  );
}
