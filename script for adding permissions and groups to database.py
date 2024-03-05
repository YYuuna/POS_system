from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from manager.models import Employee  # Import your models as needed

# Create or get the content types for your models
my_model_content_type = ContentType.objects.get_for_model(Employee)

# Define permissions
manage_users_permission, created = Permission.objects.get_or_create(
    codename='manage_users',
    content_type=my_model_content_type,
    defaults={'name': 'Managing Users'}
)

manage_employees_permission, created = Permission.objects.get_or_create(
    codename='manage_employees',
    content_type=my_model_content_type,
    defaults={'name': 'Managing Employees'}
)

manage_pos_services_permission, created = Permission.objects.get_or_create(
    codename='manage_pos_services',
    content_type=my_model_content_type,
    defaults={'name': 'Managing POS Services'}
)

# Create or get the groups
admin_group, created = Group.objects.get_or_create(name='Admin')
employee_group, created = Group.objects.get_or_create(name='Employee')

# Assign permissions to groups
admin_group.permissions.add(manage_users_permission, manage_employees_permission, manage_pos_services_permission)
employee_group.permissions.add(manage_pos_services_permission)