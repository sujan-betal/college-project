import RequirePermission from "@/components/RequirePermission";
import UsersAdminTable from "@/components/UsersAdminTable";

export default function SubAdmins() {
  return (
    <RequirePermission permission="USER_VIEW">
      <UsersAdminTable role="ADMIN" title="Admins" />
    </RequirePermission>
  );
}