from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Employee, Account


class AccountRegistrationForm(UserCreationForm):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())

    class Meta:
        model = Account  # Assuming your custom account model is named Account
        fields = ('username', 'password1', 'password2', 'employee')

    def save(self, commit=True):
        account = super().save(commit=False)
        account.save()

        # Associate account with employee
        employee = self.cleaned_data['employee']
        account.employee = employee
        account.save()

        return account