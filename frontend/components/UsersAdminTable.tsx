"use client";

import { useCallback, useEffect, useState } from "react";
import { api, hasPermission } from "@/lib/api";

export default function UsersAdminTable({ role, title }: { role: string; title: string }) {
  const [users, setUsers] = useState<any[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [designation, setDesignation] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const pageSize = 10;

  const [catalog, setCatalog] = useState<{ permissions: any[]; role_templates: any[] }>({
    permissions: [],
    role_templates: [],
  });
  const [template, setTemplate] = useState("");
  const [createPerms, setCreatePerms] = useState<string[]>([]);

  const [editing, setEditing] = useState<any>(null);
  const [editPerms, setEditPerms] = useState<string[]>([]);

  const canGrant = hasPermission("ALL") || hasPermission("USER_UPDATE");
  const canCreate = hasPermission("ALL") || hasPermission("USER_CREATE");
  const canDelete = hasPermission("ALL") || hasPermission("USER_DELETE");

  const load = useCallback(async () => {
    setLoading(true);
    const res = await api.adminUsers({ page, page_size: pageSize, search, role });
    setLoading(false);
    if (res.success) {
      setUsers(res.data || []);
      setTotal(res.pagination?.total || 0);
    } else {
      setMessage(res.message || "Failed to load users");
    }
  }, [page, search, role]);

  useEffect(() => {
    load();
  }, [load]);

  useEffect(() => {
    if (!canGrant) return;
    api.adminPermissions().then((res) => {
      if (res.success) setCatalog(res.data);
    });
  }, [canGrant]);

  function applyTemplate(name: string) {
    setTemplate(name);
    const t = catalog.role_templates.find((x) => x.name === name);
    setCreatePerms(t ? t.permissions : []);
  }

  function toggleAll(list: string[], setList: (v: string[]) => void) {
    setList(list.includes("ALL") ? [] : ["ALL"]);
  }

  function toggle(list: string[], setList: (v: string[]) => void, code: string) {
    if (code === "ALL") {
      toggleAll(list, setList);
      return;
    }
    const withoutAll = list.filter((c) => c !== "ALL");
    setList(withoutAll.includes(code) ? withoutAll.filter((c) => c !== code) : [...withoutAll, code]);
  }

  const createHasAll = createPerms.includes("ALL");
  const editHasAll = editPerms.includes("ALL");

  async function createUser(e: React.FormEvent) {
    e.preventDefault();
    setMessage("");
    const res = await api.adminCreateUser({
      username,
      email: email || undefined,
      role,
      designation: role === "TEACHER" && designation ? designation : undefined,
      role_template: canGrant && template ? template : undefined,
      permissions: canGrant ? createPerms : undefined,
    });
    if (res.success) {
      setMessage(res.message);
      setUsername("");
      setEmail("");
      setDesignation("");
      setTemplate("");
      setCreatePerms([]);
      load();
    } else {
      setMessage(res.message || "Failed to create user");
    }
  }

  async function toggleStatus(u: any) {
    const next = u.status === "ACTIVE" ? "INACTIVE" : "ACTIVE";
    const res = await api.adminUpdateUserStatus(u.userid, next);
    if (res.success) load();
    else setMessage(res.message);
  }

  async function remove(u: any) {
    if (!confirm(`Delete ${u.username}?`)) return;
    const res = await api.adminDeleteUser(u.userid);
    if (res.success) load();
    else setMessage(res.message);
  }

  async function openPermissions(u: any) {
    setMessage("");
    const res = await api.adminUserPermissions(u.userid);
    if (!res.success) {
      setMessage(res.message || "Failed to load permissions");
      return;
    }
    setEditing(u);
    setEditPerms(res.data || []);
  }

  async function savePermissions() {
    const res = await api.adminSetUserPermissions(editing.userid, editPerms);
    if (res.success) {
      setMessage(`Permissions updated for ${editing.username}`);
      setEditing(null);
    } else {
      setMessage(res.message || "Failed to update permissions");
    }
  }

  return (
    <>
      <h1 className="font-display text-3xl font-black text-maroon">{title}</h1>

      {canCreate ? (
        <form onSubmit={createUser} className="mt-6 flex flex-wrap items-end gap-3 rounded-2xl border border-ink/10 bg-white p-4 shadow-sm">
          <input required placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} className="rounded-lg border border-ink/15 px-3 py-2 text-sm" />
          <input placeholder="Email (optional)" value={email} onChange={(e) => setEmail(e.target.value)} className="rounded-lg border border-ink/15 px-3 py-2 text-sm" />
          {role === "TEACHER" && (
            <input placeholder="Designation" value={designation} onChange={(e) => setDesignation(e.target.value)} className="rounded-lg border border-ink/15 px-3 py-2 text-sm" />
          )}
          {canGrant && (
            <select value={template} onChange={(e) => applyTemplate(e.target.value)} className="rounded-lg border border-ink/15 px-3 py-2 text-sm">
              <option value="">No template</option>
              {catalog.role_templates.map((t) => (
                <option key={t.id} value={t.name}>{t.name}</option>
              ))}
            </select>
          )}
          <button className="rounded-full bg-maroon px-4 py-2 text-sm font-semibold text-cream">Add {title.slice(0, -1)}</button>
          <input placeholder="Search..." value={search} onChange={(e) => { setSearch(e.target.value); setPage(1); }} className="ml-auto rounded-lg border border-ink/15 px-3 py-2 text-sm" />
        </form>
      ) : null}

      {canGrant && (
        <div className="mt-3 rounded-2xl border border-ink/10 bg-white p-4 shadow-sm">
          <div className="flex items-center justify-between">
            <p className="text-xs font-semibold tracking-widest text-ink/50">ACCESS ON CREATION</p>
            <button
              type="button"
              onClick={() => toggleAll(createPerms, setCreatePerms)}
              className={`rounded-full border px-4 py-1 text-xs font-semibold ${createHasAll ? "border-maroon bg-maroon text-cream" : "border-ink/15"}`}
            >
              {createHasAll ? "Full access ON" : "Give full access (ALL)"}
            </button>
          </div>
          <div className="mt-2 flex flex-wrap gap-2">
            {catalog.permissions.length === 0 ? (
              <p className="text-sm text-ink/50">No permissions available.</p>
            ) : (
              catalog.permissions.map((p) => (
                <button
                  key={p.id}
                  type="button"
                  onClick={() => toggle(createPerms, setCreatePerms, p.code)}
                  title={p.description || p.code}
                  className={`rounded-full border px-3 py-1 text-xs ${
                    createPerms.includes(p.code)
                      ? "border-maroon bg-maroon text-cream"
                      : "border-ink/15"
                  } ${createHasAll && p.code !== "ALL" ? "opacity-40" : ""}`}
                >
                  {p.code}
                </button>
              ))
            )}
          </div>
          {createHasAll && (
            <p className="mt-2 text-xs text-ink/50">
              Full access selected. Turn it off to pick individual permissions.
            </p>
          )}
        </div>
      )}

      {message && <p className="mt-3 text-sm text-ink/70">{message}</p>}

      <div className="mt-4 overflow-x-auto rounded-2xl border border-ink/10 bg-white shadow-sm">
        <table className="w-full min-w-[560px] text-sm">
          <thead>
            <tr className="bg-maroon text-cream">
              <th className="px-4 py-3 text-left">Username</th>
              <th className="px-4 py-3 text-left">Email</th>
              <th className="px-4 py-3 text-left">Role</th>
              <th className="px-4 py-3 text-left">Status</th>
              <th className="px-4 py-3 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={5} className="px-4 py-3">Loading...</td></tr>
            ) : users.length === 0 ? (
              <tr><td colSpan={5} className="px-4 py-3">No users found.</td></tr>
            ) : users.map((u, i) => (
              <tr key={u.userid} className={i % 2 ? "bg-cream/60" : ""}>
                <td className="px-4 py-3">{u.username}</td>
                <td className="px-4 py-3">{u.email || "-"}</td>
                <td className="px-4 py-3">{u.role}</td>
                <td className="px-4 py-3">{u.status}</td>
                <td className="px-4 py-3 space-x-2">
                  {canGrant && (
                    <button onClick={() => openPermissions(u)} className="rounded-full border border-ink/15 px-3 py-1 text-xs">
                      Access
                    </button>
                  )}
                  <button onClick={() => toggleStatus(u)} className="rounded-full border border-ink/15 px-3 py-1 text-xs">
                    {u.status === "ACTIVE" ? "Deactivate" : "Activate"}
                  </button>
                  {canDelete && (
                    <button onClick={() => remove(u)} className="rounded-full border border-red-300 px-3 py-1 text-xs text-red-600">Delete</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-4 flex items-center gap-3 text-sm">
        <button disabled={page <= 1} onClick={() => setPage(page - 1)} className="rounded border border-ink/15 px-3 py-1 disabled:opacity-40">Prev</button>
        <span>Page {page} of {Math.max(1, Math.ceil(total / pageSize))} ({total} total)</span>
        <button disabled={page * pageSize >= total} onClick={() => setPage(page + 1)} className="rounded border border-ink/15 px-3 py-1 disabled:opacity-40">Next</button>
      </div>

      {editing && (
        <div className="fixed inset-0 z-50 grid place-items-center bg-ink/50 p-4">
          <div className="w-full max-w-lg rounded-2xl bg-white p-6 shadow-xl">
            <h2 className="font-display text-xl font-bold text-maroon">Access for {editing.username}</h2>
            <p className="mt-1 text-xs text-ink/50">Give full access, or tick only what this {title.slice(0, -1).toLowerCase()} should manage.</p>
            <button
              type="button"
              onClick={() => toggleAll(editPerms, setEditPerms)}
              className={`mt-3 w-full rounded-full border px-4 py-2 text-sm font-semibold ${editHasAll ? "border-maroon bg-maroon text-cream" : "border-ink/15"}`}
            >
              {editHasAll ? "Full access ON" : "Give full access (ALL)"}
            </button>
            <div className="mt-3 max-h-72 space-y-2 overflow-y-auto">
              {catalog.permissions.map((p) => (
                <label
                  key={p.id}
                  className={`flex items-start gap-2 rounded-lg border border-ink/10 p-2 ${editHasAll && p.code !== "ALL" ? "opacity-40" : ""}`}
                >
                  <input
                    type="checkbox"
                    checked={editPerms.includes(p.code)}
                    onChange={() => toggle(editPerms, setEditPerms, p.code)}
                    className="mt-1"
                  />
                  <span>
                    <span className="text-sm font-semibold">{p.code}</span>
                    <span className="block text-xs text-ink/50">{p.description}</span>
                  </span>
                </label>
              ))}
            </div>
            <div className="mt-4 flex justify-end gap-3">
              <button onClick={() => setEditing(null)} className="rounded-full border border-ink/15 px-4 py-2 text-sm">Cancel</button>
              <button onClick={savePermissions} className="rounded-full bg-maroon px-4 py-2 text-sm font-semibold text-cream">Save</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}