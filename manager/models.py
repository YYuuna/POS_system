from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    tel = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return self.nom


class Client(models.Model):
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    tel = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True)
    adresse = models.TextField()

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Produit(models.Model):

    CHOIX_ETAT = [
        ('EN_VENTE', 'En vente'),
        ('EN_RÉPARATION', 'En réparation'),
        ('RÉPARATION_TERMINÉE', 'Réparation terminée')
    ]

    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix_achat_initiale = models.DecimalField(max_digits=10, decimal_places=2)
    prix_vente_initiale = models.DecimalField(max_digits=10, decimal_places=2)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True)
    etat = models.CharField(max_length=20, choices=CHOIX_ETAT, default='EN_VENTE')
    
    # Other fields...

    def __str__(self):
        return self.nom


class Commande(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True)
    date_commande = models.DateField(auto_now_add=True)
    date_delivraison = models.DateField(null=True, blank=True)
    delivre = models.BooleanField(default=False)
    # Other fields...

    def __str__(self):
        return f"Purchase Order #{self.pk} - Supplier: {self.fournisseur.nom}"


class ArticleCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2)  # Dynamic price for purchase order
    # Other fields...

    def __str__(self):
        return f"Purchase Order Item #{self.pk} - produit: {self.produit.nom}"

    class Meta:
        unique_together = ('order', 'produit')


class Vente(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    date_achat = models.DateField(auto_now_add=True)
    # Other fields...

    def __str__(self):
        return f"Sale #{self.pk} - Client: {self.client.prenom} {self.client.nom}"


class ArticleVente(models.Model):
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)  # Dynamic price for sale
    # Other fields...

    def __str__(self):
        return f"Sale Item #{self.pk} - produit: {self.produit.nom}"

    class Meta:
        unique_together = ('sale', 'produit')


class Reparation(models.Model):
    CHOIX_ETAT = [
        ('EN_COURS', 'En cours'),
        ('TERMINÉ', 'Terminé')
    ]

    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    date_reparation = models.DateField(auto_now_add=True)
    etat = models.CharField(max_length=20, choices=CHOIX_ETAT, default='EN_COURS')
    # Other fields...

    def __str__(self):
        return f"Reparation pour produit: {self.produit.nom}, Client: {self.client.prenom} {self.client.nom}"


class Employe(models.Model):
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    salaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tel = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True)
    adresse = models.TextField()

    def __str__(self):
        return f"{self.prenom} {self.nom}"
