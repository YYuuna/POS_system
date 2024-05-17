from django.core.validators import MinValueValidator
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
    is_active = models.BooleanField(_('Active'), db_column='Actif', default=True)
    date_joined = models.DateTimeField(_('Date joined'), db_column='Date d\'adhésion', auto_now_add=True)

    groups = models.ManyToManyField(Group, verbose_name=_('Groups'), blank=True)

    employee = models.OneToOneField('Employee', on_delete=models.CASCADE, db_column='Employé', null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'Compte'
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
        elif employee.role == 'Repairer':
            instance.groups.add(Group.objects.get(name='Repairer'))


class Supplier(models.Model):
    name = models.CharField(max_length=100, db_column='Nom')
    phone = PhoneNumberField(unique=True, region='DZ', db_column='Téléphone')
    email = models.EmailField(unique=True, db_column='Email')
    address = models.TextField(db_column='Adresse')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Fournisseur'


class Client(models.Model):
    first_name = models.CharField(max_length=100, db_column='Prénom')
    last_name = models.CharField(max_length=100, db_column='Nom')
    phone = PhoneNumberField(unique=True, region='DZ', db_column='Téléphone')
    email = models.EmailField(unique=True, db_column='Email')
    address = models.TextField(db_column='Adresse')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'Client'


class Category(models.Model):
    name = models.CharField(max_length=100, db_column='Nom')


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Catégorie'


class Product(models.Model):
    # STATE_CHOICES = [
    #     ('En vente', 'En vente'),
    #     ('En réparation', 'En réparation'),
    #     ('RÉPARATION_TERMINÉE', 'Réparation terminée')
    # ]

    name = models.CharField(max_length=100, db_column='Nom', unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1, db_column='Catégorie')
    description = models.TextField(db_column='Description', default='Pas de description')
    # state = models.CharField(max_length=20, choices=STATE_CHOICES, default='En vente', db_column='État')
    quantity = models.PositiveIntegerField(default=0, blank=True, null=True, db_column='Quantité')
    # initial_buying_price = models.PositiveIntegerField(blank=True, null=True,
    #                                            db_column='Prix d\'achat initiale')
    initial_selling_price = models.PositiveIntegerField(default=0, db_column='Prix de vente initiale')
    #supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL,null=True, db_column='Fournisseur')
    suppliers = models.ManyToManyField(Supplier, through='Suppliying', db_column='Fournisseurs', related_name='products')
    # Other fields...

    def __str__(self):
        return self.name

    def form_field_representation(self):
        return f"{self.id} - {self.name}"

    class Meta:
        db_table = 'Produit'
        verbose_name = _('Produit')

class Suppliying(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='Produit')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, db_column='Fournisseur')

    class Meta:
        db_table = 'Fournir'  # change this to your desired table name

class PurchaseOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, db_column='Fournisseur')
    order_date = models.DateField(auto_now_add=True, db_column='Date de commande')
    delivery_date = models.DateField(null=True, blank=True, db_column='Date de livraison')
    # is_delivered = models.BooleanField(default=False, db_column='Est livré')

    # Other fields...

    def __str__(self):
        str=f"Purchase Order #{self.pk} - Supplier: "
        if self.supplier:
            str+=self.supplier.name
        else:
            str+="Fournisseur inconnu"
        return str

    class Meta:
        db_table = 'Commande'


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, db_column='Commande')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='Produit')
    quantity = models.PositiveIntegerField(db_column='Quantité', validators=[MinValueValidator(1, message="La quantité doit être supérieure à 0")])
    purchase_price = models.PositiveIntegerField(null=True,blank=True,db_column='Prix d\'achat')  # Dynamic price for purchase order

    # Other fields...

    def __str__(self):
        return f"Purchase Order Item #{self.pk} - Product: {self.product.name}"

    class Meta:
        db_table = 'ArticleCommande'
        #unique_together = ('purchase_order', 'product')


class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, db_column='Client')
    sale_date = models.DateField(auto_now_add=True, db_column='Date de vente')

    # Other fields...

    def __str__(self):
        return f"Sale #{self.pk} - Client: {self.client.first_name} {self.client.last_name}"

    class Meta:
        db_table = 'Vente'

    def delete_sale(self, update_product_quantity=False):
        # Get the related SaleItem instances
        sale_items = self.saleitem_set.all()

        # Iterate over the SaleItem instances
        for sale_item in sale_items:
            # Delete the SaleItem with updating the product quantity
            sale_item.delete(update_product_quantity=update_product_quantity)

        # Delete the Sale instance
        super().delete()


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, db_column='Vente')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='Produit')
    quantity = models.PositiveIntegerField(db_column='Quantité', validators=[MinValueValidator(1, message="La quantité doit être supérieure à 0")])
    sale_price = models.PositiveIntegerField(db_column='Prix de vente')  # Dynamic price for sale

    # Other fields...

    def __str__(self):
        return f"Sale Item #{self.pk} - Product: {self.product.name}"

    class Meta:
        db_table = 'ArticleVente'
        #unique_together = ('sale', 'product')

    def save(self, *args, **kwargs):
        # If the SaleItem already exists in the database
        if self.pk:
            # Get the old SaleItem from the database
            old_sale_item = SaleItem.objects.get(pk=self.pk)

            # If the quantity has been updated
            if old_sale_item.quantity != self.quantity:
                # Update the product's quantity
                self.product.quantity += old_sale_item.quantity - self.quantity
                self.product.save()

        else:  # If the SaleItem is new
            self.product.refresh_from_db()
            # Decrease the product's quantity
            self.product.quantity -= self.quantity
            self.product.save()

        super().save(*args, **kwargs)

    def delete(self, update_product_quantity=True, *args, **kwargs):
        if update_product_quantity:
            # Increase the product's quantity
            self.product.quantity += self.quantity
            self.product.save()

        super().delete(*args, **kwargs)


class Repair(models.Model):
    STATE_CHOICES = [
        ('En cours', 'En cours'),
        ('Terminé', 'Terminé')
    ]
    title = models.CharField(max_length=100, default='Pas de description',db_column='Titre')
    description = models.TextField(db_column='Description')
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='En cours', db_column='État')
    hardware = models.OneToOneField('HardwareToRepair', db_column='Matériel',on_delete=models.CASCADE)
    deposit_date = models.DateField(auto_now_add=True, db_column='Date de dépôt')
    delivery_date = models.DateField(null=True, blank=True, db_column='Date de remise')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, db_column='Client')
    prepayment = models.PositiveIntegerField(db_column='Acompte',default=0)
    repair_price = models.PositiveIntegerField(db_column='Prix de réparation',default=0)

    # Other fields...

    def __str__(self):
        return f"Repair for Product: {self.product.name}, Client: {self.client.first_name} {self.client.last_name}"

    class Meta:
        db_table = 'Réparation'


class Employee(models.Model):
    first_name = models.CharField(max_length=100, db_column='Prénom')
    last_name = models.CharField(max_length=100, db_column='Nom')
    phone = PhoneNumberField(unique=True, region='DZ', db_column='Téléphone')
    email = models.EmailField(unique=True, db_column='Email')
    address = models.TextField(db_column='Adresse')
    ROLES_CHOICES = [
        ('Admin', _('Admin')),
        ('Employé', _('Employé')),
         ('Réparateur', _('Réparateur')),
    ]
    role = models.CharField(_('Role'), max_length=100, choices=ROLES_CHOICES, default='Employé', db_column='Rôle')
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='Salaire')
    class Meta:
        db_table = 'Employé'
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # check if the object exists in the database
        if self.pk is not None:
            orig = Employee.objects.get(pk=self.pk)
            if orig.role != self.role:  # if role has been updated
                account = self.account  # assuming 'account' is the related_name for the OneToOne field in Account model

                new_group = Group.objects.get(name=self.role)  # replace 'new_group' with the actual group
                account.groups.clear()  # remove the account from all groups
                account.groups.add(new_group)  # add the account to the new group
                account.save()
        super(Employee, self).save(*args, **kwargs)

class HardwareToRepair(models.Model):
    name = models.CharField(max_length=100, db_column='Nom')
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1, db_column='Catégorie')
    description = models.TextField(db_column='Description')
    state = models.CharField(max_length=20, default='En réparation', db_column='État')
    def __str__(self):
        return f"{self.name}"

    def form_field_representation(self):
        return f"{self.id} - {self.name}"

    class Meta:
        db_table = 'MatérielARéparer'
