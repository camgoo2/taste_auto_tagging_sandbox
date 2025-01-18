resource "google_project_iam_member" "service_account_roles" {
    project = var.project_id
    count = length(var.roles_list)
    role =  var.roles_list[count.index]
    member = "serviceAccount:${var.service_account_email}"
}
