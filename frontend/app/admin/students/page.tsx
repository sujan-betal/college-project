import RequirePermission from "@/components/RequirePermission";
import UsersAdminTable from "@/components/UsersAdminTable";

export default function AdminStudents() {
  return (
    <RequirePermission permission="USER_VIEW">
      <UsersAdminTable role="STUDENT" title="Students" />
    </RequirePermission>
  );
}
