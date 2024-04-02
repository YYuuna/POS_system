from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, TemplateView
from django.urls import reverse_lazy
from .models import Client, Supplier, Product, Account, Employee, PurchaseOrder, Sale, Repair, Category, SaleItem, \
    PurchaseOrderItem
from .forms import ClientForm, UserLoginForm, FilterForm, SupplierForm, ProductForm, AccountRegistrationForm, \
    EmployeeForm, CategoryForm, SaleForm, SaleItemFormSet, SaleItemForm, PurchaseOrderForm, PurchaseOrderItemFormSet, \
    PurchaseOrderItemForm


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
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(id=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm(self.request.GET)
        return context


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'modifierclient.html'
    success_url = reverse_lazy('client-list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'supprimerclient.html'
    success_url = reverse_lazy('client-list')


class AddSupplierView(LoginRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'ajouterfournisseur.html'
    success_url = reverse_lazy('supplier-list')


class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'listefournisseur.html'
    context_object_name = 'suppliers'
    paginate_by = 10
    form_class = FilterForm

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(id=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm(self.request.GET)
        return context


class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'supplier_update_form.html'
    success_url = reverse_lazy('supplier-list')


class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'supplier_confirm_delete.html'
    success_url = reverse_lazy('supplier-list')


class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'ajouterproduit.html'
    success_url = reverse_lazy('product-list')


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'listeproduit.html'  # replace with your template
    context_object_name = 'products'
    paginate_by = 10
    form_class = FilterForm

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(id=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm(self.request.GET)
        return context


class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, 'detaillproduit.html', {'product': product})


class AccountListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Account
    template_name = 'listecompte.html'
    context_object_name = 'accounts'
    paginate_by = 10
    form_class = FilterForm

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(id=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm(self.request.GET)
        return context

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'avez pas la permission d'accéder à cette page.")
        return redirect('dashboard')


class PurchaseOrderListView(LoginRequiredMixin, ListView):
    model = PurchaseOrder
    template_name = 'listecommande.html'
    context_object_name = 'purchase_orders'
    paginate_by = 10
    form_class = FilterForm

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(id=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm(self.request.GET)
        return context


class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'listevente.html'
    context_object_name = 'sales'
    paginate_by = 10
    form_class = FilterForm

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(id=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm(self.request.GET)
        return context


class RepairListView(LoginRequiredMixin, ListView):
    model = Repair
    template_name = 'listereparation.html'
    context_object_name = 'repairs'
    paginate_by = 10
    form_class = FilterForm

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(id=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm(self.request.GET)
        return context


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'menu.html'


class DashboardView(TemplateView):
    pass


class AddAccountView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Account
    form_class = AccountRegistrationForm
    template_name = 'ajoutercompte.html'
    success_url = reverse_lazy('account-list')

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'avez pas la permission d'accéder à cette page.")
        return redirect('dashboard')


class AccountUpdateView(LoginRequiredMixin, UserPassesTestMixin, PasswordChangeView):
    model = Account
    form_class = PasswordChangeForm
    template_name = 'modifiercompte.html'
    success_url = reverse_lazy('account-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = Account.objects.get(pk=self.kwargs['pk'])
        return kwargs

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'avez pas la permission d'accéder à cette page.")
        return redirect('dashboard')


class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Account
    template_name = 'supprimercompte.html'
    success_url = reverse_lazy('account-list')

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'avez pas la permission d'accéder à cette page.")
        return redirect('dashboard')


class AddEmployeeView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'ajouteremploye.html'
    success_url = reverse_lazy('employee-list')

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'avez pas la permission d'accéder à cette page.")
        return redirect('dashboard')


class EmployeeListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Employee
    template_name = 'listeemploye.html'
    context_object_name = 'employees'
    paginate_by = 10
    form_class = FilterForm

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(id=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm(self.request.GET)
        return context

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'avez pas la permission d'accéder à cette page.")
        return redirect('dashboard')


class EmployeeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'modifieremploye.html'
    success_url = reverse_lazy('employee-list')

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'avez pas la permission d'accéder à cette page.")
        return redirect('dashboard')


class EmployeeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Employee
    template_name = 'supprimeremploye.html'
    success_url = reverse_lazy('employee-list')

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def handle_no_permission(self):
        messages.error(self.request, "Vous n'avez pas la permission d'accéder à cette page.")
        return redirect('dashboard')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'modifierproduit.html'
    success_url = reverse_lazy('product-list')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'supprimerproduit.html'
    success_url = reverse_lazy('product-list')


class AddCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'cat.html'
    success_url = reverse_lazy('add-product')


class TestView(LoginRequiredMixin, TemplateView):
    template_name = 'pdf.html'


class AddSaleView(LoginRequiredMixin, CreateView):
    model = Sale
    template_name = 'ajoutervente.html'
    form_class = SaleForm

    def form_valid(self, form):
        self.object = form.save()
        return redirect('update-sale', pk=self.object.pk)

    def get_success_url(self):
        return reverse_lazy('update-sale', kwargs={'pk': self.object.pk})


class SaleUpdateView(LoginRequiredMixin, FormView):
    template_name = 'articlevente.html'
    success_url = reverse_lazy('sale-list')
    form_class = SaleItemFormSet

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = Sale.objects.get(pk=self.kwargs['pk'])
        sale = Sale.objects.get(pk=self.kwargs['pk'])
        kwargs['queryset'] = SaleItem.objects.filter(sale=sale)
        kwargs['form_kwargs'] = {'sale': sale}  # Pass the Sale instance to the SaleItemForm
        return kwargs

    def form_valid(self, form):
        instances = form.save(commit=False)
        for instance in form.deleted_objects:
            instance.delete()
        for instance in instances:
            instance.save()
        # Clear the submitted_products list
        SaleItemForm.submitted_products.clear()

        return super().form_valid(form)

    def form_invalid(self, form):
        # Clear the submitted_products list
        SaleItemForm.submitted_products.clear()
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)


# class SaleDeleteView(LoginRequiredMixin, DeleteView):
#     model = Sale
#     template_name = 'supprimervente.html'
#     success_url = reverse_lazy('sale-list')
#
#     def delete(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         self.object.delete_sale()
#         return super().delete(request, *args, **kwargs)


class SaleCancelView(LoginRequiredMixin, DeleteView):
    model = Sale
    template_name = 'supprimervente.html'
    success_url = reverse_lazy('sale-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete_sale(
            update_product_quantity=True)  # Call the delete_sale method with update_product_quantity=True
        return super().delete(request, *args, **kwargs)


class ProductInitialSellingPriceView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            product = Product.objects.get(pk=pk)
            return JsonResponse({'initial_selling_price': product.initial_selling_price})
        except Product.DoesNotExist:
            raise Http404("Product does not exist")

class AddPurchaseOrderView(LoginRequiredMixin, CreateView):
    model = PurchaseOrder
    template_name = 'ajoutercommande.html'
    form_class = PurchaseOrderForm
    success_url = reverse_lazy('purchase-order-list')

    def form_valid(self, form):
        self.object = form.save()
        return redirect('update-purchase-order', pk=self.object.pk)

    def get_success_url(self):
        return reverse_lazy('update-purchase-order', kwargs={'pk': self.object.pk})


class PurchaseOrderUpdateView(LoginRequiredMixin, FormView):
    template_name = 'articlecommande.html'
    success_url = reverse_lazy('purchase-order-list')
    form_class = PurchaseOrderItemFormSet

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = PurchaseOrder.objects.get(pk=self.kwargs['pk'])
        purchase_order = PurchaseOrder.objects.get(pk=self.kwargs['pk'])
        kwargs['queryset'] = PurchaseOrderItem.objects.filter(purchase_order=purchase_order)
        return kwargs

    def form_valid(self, form):
        instances = form.save(commit=False)
        for instance in form.deleted_objects:
            instance.delete()
        for instance in instances:
            instance.save()
        # Clear the submitted_products list
        PurchaseOrderItemForm.submitted_products.clear()
        return super().form_valid(form)

    def form_invalid(self, form):
        # Clear the submitted_products list
        PurchaseOrderItemForm.submitted_products.clear()
        return super().form_invalid(form)


class PurchaseOrderDeleteView(LoginRequiredMixin, DeleteView):
    model = PurchaseOrder
    template_name = 'supprimercommande.html'
    success_url = reverse_lazy('purchase-order-list')

class ProductInitialPurchasePriceView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            product = Product.objects.get(pk=pk)
            return JsonResponse({'initial_buying_price': product.initial_buying_price})
        except Product.DoesNotExist:
            raise Http404("Product does not exist")