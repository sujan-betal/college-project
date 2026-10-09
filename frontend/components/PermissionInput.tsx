"use client";

import { useCallback, useEffect, useState } from "react";
import { api } from "@/lib/api";

// Permission names are plain text — no catalog, no ids. This box lets an
// admin type names (comma or space separated) and shows which ones are set.
export default function PermissionInput({
  value,
  onChange,
  suggestions = [],
  label = "Permissions",
  hint = "Comma separated. Use ALL for full access.",
}: {
  value: string[];
  onChange: (next: string[]) => void;
  suggestions?: string[];
  label?: string;
  hint?: string;
}) {
  const [text, setText] = useState(value.join(", "));

  useEffect(() => {
    setText(value.join(", "));
  }, [value.join(", ")]);

  const apply = useCallback(
    (raw: string) => {
      const names = Array.from(
        new Set(
          raw
            .split(/[,\s]+/)
            .map((n) => n.trim().toUpperCase())
            .filter(Boolean)
        )
      );
      onChange(names.includes("ALL") ? ["ALL"] : names);
    },
    [onChange]
  );

  return (
    <div>
      <p className="text-xs font-semibold tracking-widest text-ink/50">{label}</p>
      <input
        value={text}
        onChange={(e) => {
          setText(e.target.value);
          apply(e.target.value);
        }}
        placeholder="USER_VIEW, FEE_VIEW"
        list="permission-suggestions"
        className="mt-1 w-full rounded-lg border border-ink/15 px-3 py-2 text-sm"
      />
      <datalist id="permission-suggestions">
        {suggestions.map((s) => (
          <option key={s} value={s} />
        ))}
      </datalist>

      <div className="mt-2 flex flex-wrap gap-1">
        {value.length === 0 ? (
          <span className="text-xs text-ink/40">None</span>
        ) : (
          value.map((name) => (
            <button
              key={name}
              type="button"
              onClick={() => {
                const next = value.filter((n) => n !== name);
                onChange(next);
                setText(next.join(", "));
              }}
              className={`rounded-full border px-2 py-0.5 text-[10px] font-semibold ${
                name === "ALL" ? "border-maroon bg-maroon text-cream" : "border-ink/15 text-ink/70"
              }`}
            >
              {name} ×
            </button>
          ))
        )}
      </div>

      <p className="mt-1 text-xs text-ink/50">{hint}</p>
    </div>
  );
}