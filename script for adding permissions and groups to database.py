from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from manager.models import Employee ,Account # Import your models as needed

# Create or get the content types for your models
employee_content_type = ContentType.objects.get_for_model(Employee)
account_content_type = ContentType.objects.get_for_model(Account)

# Define permissions
manage_users_permission, created = Permission.objects.get_or_create(
    codename='manage_accounts',
    content_type=account_content_type,
    defaults={'name': 'Managing Accounts'}
)

manage_employees_permission, created = Permission.objects.get_or_create(
    codename='manage_employees',
    content_type=employee_content_type,
    defaults={'name': 'Managing Employees'}
)

manage_pos_services_permission, created = Permission.objects.get_or_create(
    codename='manage_pos_services',
    content_type=employee_content_type,
    defaults={'name': 'Managing POS Services'}
)

manage_repair_services_permission, created = Permission.objects.get_or_create(
    codename='manage_repair_services',
    content_type=employee_content_type,
    defaults={'name': 'Managing Repair Services'}
)

# Create or get the groups
admin_group, created = Group.objects.get_or_create(name='Admin')
employee_group, created = Group.objects.get_or_create(name='Employé')
repairer_group, created = Group.objects.get_or_create(name='Réparateur')
# Assign permissions to groups
admin_group.permissions.add(manage_users_permission, manage_employees_permission, manage_pos_services_permission)
employee_group.permissions.add(manage_pos_services_permission)
repairer_group.permissions.add(manage_repair_services_permission)