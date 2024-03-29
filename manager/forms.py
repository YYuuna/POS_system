from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Employee, Account, Client, Supplier, Product, Category


class AccountRegistrationForm(UserCreationForm):
    employee = forms.ModelChoiceField(queryset=Employee.objects.filter(account__isnull=True))

    class Meta:
        model = Account  # Assuming your custom account model is named Account
        fields = ('username', 'password1', 'password2', 'employee')
        labels = {
            'username': "",
            'password1': "",
            'password2': "",
            'employee': "Employé"
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirmer le mot de passe'}),
            'employee': forms.Select(attrs={'placeholder': 'Choisir un employé'}),
        }
        error_messages = {
            'username': {'required': 'Le nom d\'utilisateur est requis.',
                         'unique': 'Ce nom d\'utilisateur est déjà utilisé. Veuillez en choisir un autre.'},
            'password1': {'required': 'Le mot de passe est requis.'},
            'password2': {
                'required': 'Veuillez confirmer le mot de passe.',
                'password_mismatch': 'Les mots de passe ne correspondent pas.'
            },
            'employee': {'required': 'Veuillez choisir un employé.'}
        }

    def __init__(self, *args, **kwargs):
        super(AccountRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = ""
        self.fields['password2'].label = ""
        self.fields['employee'].label = "Employé"
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Mot de passe', 'autocomplete': 'new-password'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Confirmer le mot de passe', 'autocomplete': 'new-password'})

    def save(self, commit=True):
        account = super().save(commit=False)
        account.save()

        # Associate account with employee
        employee = self.cleaned_data['employee']
        account.employee = employee
        account.save()

        return account


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['last_name', 'first_name', 'phone', 'email', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Entrer le prénom'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Entrer le nom'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Entrer le numero teléphone'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Entrer l\'email'}),
            'address': forms.TextInput(attrs={'placeholder': 'Entrer l\'adresse'}),
        }
        labels = {
            'first_name': "",
            'last_name': "",
            'phone': "",
            'email': "",
            'address': "",
        }
        error_messages = {
            'first_name': {
                'required': "Le prénom du client est requis.",
                'max_length': "Le prénom du client ne peut pas dépasser %(max)d caractères.",
            },
            'last_name': {
                'required': "Le nom de famille du client est requis.",
                'max_length': "Le nom de famille du client ne peut pas dépasser %(max)d caractères.",
            },
            'phone': {
                'required': "Le numéro de téléphone est requis.",
                'invalid': "Veuillez entrer un numéro de téléphone valide.",
                'unique': "Un client avec ce numéro de téléphone existe déjà.",
            },
            'email': {
                'required': "L'adresse e-mail est requise.",
                'invalid': "Veuillez fournir une adresse e-mail valide.",
                'unique': "Un client avec cette adresse e-mail existe déjà.",
            },
            'address': {
                'required': "L'adresse est requise.",
            }
        }


class UserLoginForm(AuthenticationForm):
    remember = forms.BooleanField(required=False, label='Remember me')
    default_errors = {
        'required': "Ce champ est requis.",
        'invalid': "Valeur invalide.",
        'invalid_login': "Nom d'utilisateur ou mot de passe incorrect.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'id': 'username',
            'name': 'username',
            'class': 'input',  # Add additional classes as needed
            'placeholder': 'Entrer votre nom d\'utilisateur'
        })
        self.fields['password'].widget.attrs.update({
            'id': 'password',
            'name': 'password',
            'class': 'input',  # Add additional classes as needed
            'placeholder': 'Entrer votre mot de passe'
        })
        self.fields['remember'].widget.attrs.update({
            'id': 'remember_field_id',
            'class': 'remember_field_class',  # Add additional classes as needed
        })

    def add_error(self, field, error):
        if error == 'invalid_login':
            error = self.default_errors['invalid_login']
        super().add_error(field, error)


class FilterForm(forms.Form):
    query = forms.IntegerField(label='', required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'Rechercher par ID'}))


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'phone', 'email', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Entrer le nom de fournisseur'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Entrer le numero teléphone'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Entrer l\'email'}),
            'address': forms.TextInput(attrs={'placeholder': 'Entrer l\'adresse'}),
        }
        labels = {
            'name': "",
            'phone': "",
            'email': "",
            'address': "",
        }
        error_messages = {
            'name': {
                'required': "Le nom du fournisseur est requis.",
                'max_length': "Le nom du fournisseur ne peut pas dépasser %(max)d caractères.",
            },
            'phone': {
                'required': "Le numéro de téléphone est requis.",
                'invalid': "Veuillez entrer un numéro de téléphone valide.",
                'unique': "Un fournisseur avec ce numéro de téléphone existe déjà.",
            },
            'email': {
                'required': "L'adresse e-mail est requise.",
                'invalid': "Veuillez fournir une adresse e-mail valide.",
                'unique': "Un fournisseur avec cette adresse e-mail existe déjà.",
            },
            'address': {
                'required': "L'adresse est requise.",
            }
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'state', 'initial_buying_price', 'initial_selling_price',
                  'supplier']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Entrer le nom du produit'}),
            'category': forms.Select(attrs={'placeholder': 'Choisir la catégorie du produit'}),
            # Add 'size': 3 as needed
            # Add 'rows': 3, 'cols': 30 as needed
            'state': forms.Select(attrs={'placeholder': 'Choisir l\'état du produit'}, choices=[
                ('EN_VENTE', 'En vente'),
                ('EN_REPARATION', 'En réparation')
                # do not include 'reparation_terminee' here
            ]),  # Add 'size': 3 as needed
            'initial_buying_price': forms.NumberInput(attrs={'placeholder': 'Entrer le prix d\'achat'}),
            'initial_selling_price': forms.NumberInput(attrs={'placeholder': 'Entrer le prix de vente'}),
            'supplier': forms.Select(attrs={'placeholder': 'Choisir le fournisseur'}),
        }
        labels = {
            'name': "",
            'category': 'Choisir la catégorie du produit',
            'state': 'Choisir l\'état du produit',
            'initial_buying_price': "",
            'initial_selling_price': "",
            'supplier': "Choisir le fournisseur",
        }
        error_messages = {
            'name': {
                'required': "Le nom du produit est requis.",
                'max_length': "Le nom du produit ne peut pas dépasser %(max)d caractères.",
            },
            'category': {
                'required': "La catégorie du produit est requise.",
            },
            'description': {
                'required': "La description du produit est requise.",
            },
            'state': {
                'required': "Le statut du produit est requis.",
            },
            'initial_buying_price': {
                'required': "Le prix d'achat est requis.",
                'invalid': "Veuillez entrer un prix d'achat valide.",
            },
            'initial_selling_price': {
                'required': "Le prix de vente est requis.",
                'invalid': "Veuillez entrer un prix de vente valide.",
            },
            'supplier': {
                'required': "Le fournisseur est requis.",
            }
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['state'].choices = [(key, value) for key, value in Product.STATE_CHOICES if
                                            key != 'RÉPARATION_TERMINÉE']


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'salary', 'phone', 'email', 'address', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Entrez le prénom'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Entrez le nom'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Entrez le numéro de téléphone'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Entrez l\'email'}),
            'address': forms.TextInput(attrs={'placeholder': 'Entrez l\'adresse'}),
            'role': forms.Select(attrs={'placeholder': 'Sélectionnez le rôle'}),
            'salary': forms.NumberInput(attrs={'placeholder': 'Entrez le salaire'}),
        }
        labels = {
            'first_name': "",
            'last_name': "",
            'phone': "",
            'email': "",
            'address': "",
            'salary': "",
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Entrer une nouvelle catégorie'}),

        }
        labels = {
            'name': "",

        }
