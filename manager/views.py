from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy
from .models import Client, Supplier
from .forms import ClientForm, UserLoginForm, FilterForm, SupplierForm


class AddClientView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client_form.html'
    success_url = reverse_lazy('client-list')


class UserLoginView(LoginView):
    template_name = 'login.html'  # Specify the template for the login page
    form_class = UserLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        remember = form.cleaned_data.get('remember')
        if remember:
            self.request.session.set_expiry(None)  # Session will persist even after browser is closed
        else:
            self.request.session.set_expiry(0)  # Session will expire when browser is closed
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'listeclient.html'
    context_object_name = 'clients'
    form_class = FilterForm

    def get_queryset(self):
        queryset = super().get_queryset()
        client_id = self.request.GET.get('client_id')
        if client_id:
            queryset = queryset.filter(id=client_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm(self.request.GET)
        return context

class ClientUpdateView(UpdateView):
    model = Client
    fields = ['last_name', 'first_name', 'phone', 'email', 'address']
    template_name = 'client_update_form.html'
    success_url = reverse_lazy('client_list')

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'client_confirm_delete.html'
    success_url = reverse_lazy('client_list')
class AddSupplierView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'ajouterfournisseur.html'
    success_url = reverse_lazy('supplier-list')
