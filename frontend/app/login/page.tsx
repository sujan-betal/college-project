export default function Login() {
  return (
    <section className="grain bg-maroon text-cream">
      <div className="mx-auto flex min-h-[70vh] max-w-md flex-col justify-center px-4 py-16">
        <h1 className="font-display text-4xl font-black">Portal Login</h1>
        <p className="mt-2 text-cream/80">
          One login for students, teachers, and administrators. Your role decides
          where you land.
        </p>
        <form className="mt-8 space-y-4 rounded-2xl bg-cream p-6 text-ink shadow-xl">
          <input required placeholder="Username or email" className="w-full rounded-lg border border-ink/15 px-4 py-2.5" />
          <input required type="password" placeholder="Password" className="w-full rounded-lg border border-ink/15 px-4 py-2.5" />
          <div className="flex items-center justify-between text-xs text-ink/60">
            <label className="flex items-center gap-2">
              <input type="checkbox" /> Remember me
            </label>
            <a href="#" className="text-maroon font-semibold">Forgot password?</a>
          </div>
          <button className="w-full rounded-full bg-maroon py-3 font-semibold text-cream hover:bg-maroon-dark transition">
            Sign In
          </button>
          <p className="text-center text-xs text-ink/50">Design preview — authentication connects to the backend later.</p>
        </form>
      </div>
    </section>
  );
}
