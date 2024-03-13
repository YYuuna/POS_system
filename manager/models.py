from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, Permission


# Model pour la gestion des comptes, il faut le définir pour django
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(_('The "Username" field must be set'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


# Compte
class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('Username'), max_length=150, unique=True)
    is_active = models.BooleanField(_('Active'), default=True)
    date_joined = models.DateTimeField(_('Date joined'), auto_now_add=True)

    groups = models.ManyToManyField(Group, verbose_name=_('Groups'), blank=True)

    employee = models.OneToOneField('Employee', on_delete=models.CASCADE, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    def __str__(self):
        return self.username


# Signal to update groups in Account model based on role in Employee model
@receiver(post_save, sender=Account)
def update_account_groups(sender, instance, created, **kwargs):
    if created and instance.employee:
        employee = instance.employee
        if employee.role == 'Admin':
            instance.groups.add(Group.objects.get(name='Admin'))
        elif employee.role == 'Employee':
            instance.groups.add(Group.objects.get(name='Employee'))


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    phone = PhoneNumberField(unique=True,region='DZ')
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return self.name


class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = PhoneNumberField(unique=True,region='DZ')
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.name

class Product(models.Model):
    STATUS_CHOICES = [
        ('EN_VENTE', 'En vente'),
        ('EN_RÉPARATION', 'En réparation'),
        ('RÉPARATION_TERMINÉE', 'Réparation terminée')
    ]

    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EN_VENTE')
    quantity = models.PositiveIntegerField(default=0,blank=True, null=True)
    initial_buying_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    initial_selling_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)

    # Other fields...

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField(null=True, blank=True)
    is_delivered = models.BooleanField(default=False)

    # Other fields...

    def __str__(self):
        return f"Purchase Order #{self.pk} - Supplier: {self.supplier.name}"


class PurchaseOrderItem(models.Model):
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)  # Dynamic price for purchase order

    # Other fields...

    def __str__(self):
        return f"Purchase Order Item #{self.pk} - Product: {self.product.name}"

    class Meta:
        unique_together = ('order', 'product')


class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    sale_date = models.DateField(auto_now_add=True)

    # Other fields...

    def __str__(self):
        return f"Sale #{self.pk} - Client: {self.client.first_name} {self.client.last_name}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)  # Dynamic price for sale

    # Other fields...

    def __str__(self):
        return f"Sale Item #{self.pk} - Product: {self.product.name}"

    class Meta:
        unique_together = ('sale', 'product')


class Repair(models.Model):
    STATUS_CHOICES = [
        ('EN_COURS', 'En cours'),
        ('TERMINÉ', 'Terminé')
    ]

    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    repair_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EN_COURS')

    # Other fields...

    def __str__(self):
        return f"Repair for Product: {self.product.name}, Client: {self.client.first_name} {self.client.last_name}"


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    phone = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()
    ROLES_CHOICES = [
        ('ADMIN', _('Admin')),
        ('EMPLOYEE', _('Employee')),
    ]
    role = models.CharField(_('Role'), max_length=100, choices=ROLES_CHOICES, default='EMPOYEE')

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
