import RequirePermission from "@/components/RequirePermission";
import UsersAdminTable from "@/components/UsersAdminTable";

export default function AdminTeachers() {
  return (
    <RequirePermission permission="USER_VIEW">
      <UsersAdminTable role="TEACHER" title="Teachers" />
    </RequirePermission>
  );
}
