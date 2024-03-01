from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    phone = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return self.name


class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('TÉLÉPHONE', 'Téléphone'),
        ('PC', 'PC'),
        ('TABLETTE', 'Tablette'),
        ('ACCESSOIRE', 'Accessoire'),
        ('APPAREIL_PHOTO', 'Appareil photo'),
        ('AUTRE', 'Autre')
    ]

    STATUS_CHOICES = [
        ('EN_VENTE', 'En vente'),
        ('EN_RÉPARATION', 'En réparation'),
        ('RÉPARATION_TERMINÉE', 'Réparation terminée')
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    initial_buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    initial_selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EN_VENTE')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
