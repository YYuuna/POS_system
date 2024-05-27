from io import BytesIO

from django.db.models import Sum, F
from django.template.loader import render_to_string
from django.utils import timezone

from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.contrib import messages
from django.http import JsonResponse, Http404, FileResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, TemplateView, DetailView
from django.urls import reverse_lazy, reverse
from weasyprint import HTML

from .models import Client, Supplier, Product, Account, Employee, PurchaseOrder, Sale, Repair, Category, SaleItem, \
    PurchaseOrderItem, HardwareToRepair
from .forms import ClientForm, UserLoginForm, FilterForm, SupplierForm, ProductForm, AccountRegistrationForm, \
    EmployeeForm, CategoryForm, SaleForm, SaleItemFormSet, SaleItemForm, PurchaseOrderForm, PurchaseOrderItemFormSet, \
    PurchaseOrderItemForm, RepairForm, CustomSetPasswordForm, HardwareToRepairForm, PurchaseOrderItemDeliveredFormSet


class RoleRequiredMixin(AccessMixin):
    """Verify that the current user has the required role."""
    required_roles = []  # Define this in your view

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.required_roles:  # if no role is required, continue
            return super().dispatch(request, *args, **kwargs)
        if not request.user.employee.role in self.required_roles:
            messages.error(request, 'Vous n\'avez pas la permission de consulter cette page.')
            return redirect('dashboard')  # or wherever
        return super().dispatch(request, *args, **kwargs)


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

class AddClientView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client_form.html'
    success_url = reverse_lazy('client-list')

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'listeclient.html'
    context_object_name = 'clients'
    form_class = FilterForm
    paginate_by = 7

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

class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'detaillclient.html'
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = get_object_or_404(Client, pk=self.kwargs['pk'])
        context['num_sales'] = Sale.objects.filter(client=client).count()
        context['num_repairs'] = Repair.objects.filter(client=client).count()
        context['rest_to_pay'] = Repair.objects.filter(client=client, delivery_date=None).annotate(to_pay=F('repair_price') - F('prepayment')).aggregate(rest_to_pay=Sum('to_pay'))['rest_to_pay'] or 0
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

class ClientSalesListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Sale
    template_name = 'listeventeclient.html'
    context_object_name = 'sales'
    paginate_by = 7
    required_roles = ['Admin', 'Employé']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm(self.request.GET)
        client = get_object_or_404(Client, pk=self.kwargs['pk'])
        context['client'] = client
        return context

    def get_queryset(self):
        client = get_object_or_404(Client, pk=self.kwargs['pk'])
        queryset = Sale.objects.filter(client=client)
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(id=query)
        return queryset

class ClientRepairsListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Repair
    template_name = 'listereparationclient.html'
    context_object_name = 'repairs'
    paginate_by = 7
    required_roles = ['Admin', 'Réparateur']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm(self.request.GET)
        client = get_object_or_404(Client, pk=self.kwargs['pk'])
        context['client'] = client
        return context

    def get_queryset(self):
        client = get_object_or_404(Client, pk=self.kwargs['pk'])
        queryset = Repair.objects.filter(client=client)
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(id=query)
        return queryset


class AddSupplierView(LoginRequiredMixin,RoleRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'ajouterfournisseur.html'
    success_url = reverse_lazy('supplier-list')
    required_roles = ['Admin', 'Employé']


class SupplierListView(LoginRequiredMixin,RoleRequiredMixin, ListView):
    model = Supplier
    template_name = 'listefournisseur.html'
    context_object_name = 'suppliers'
    paginate_by = 7
    form_class = FilterForm
    required_roles = ['Admin', 'Employé']

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

class SupplierDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    model = Supplier
    template_name = 'detaillfournisseur.html'
    context_object_name = 'supplier'
    required_roles = ['Admin', 'Employé']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supplier = get_object_or_404(Supplier, pk=self.kwargs['pk'])
        context['num_purchase_orders'] = PurchaseOrder.objects.filter(supplier=supplier).count()
        return context

class SupplierUpdateView(LoginRequiredMixin,RoleRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'modifierfournisseur.html'
    success_url = reverse_lazy('supplier-list')
    required_roles = ['Admin', 'Employé']


class SupplierDeleteView(LoginRequiredMixin,RoleRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'supprimerfournisseur.html'
    success_url = reverse_lazy('supplier-list')
    required_roles = ['Admin', 'Employé']

class SupplierPurchaseOrdersListView(LoginRequiredMixin,RoleRequiredMixin, ListView):
    model = PurchaseOrder
    template_name = 'listecommandefournisseur.html'
    context_object_name = 'purchase_orders'
    paginate_by = 7
    required_roles = ['Admin', 'Employé']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm(self.request.GET)
        supplier = get_object_or_404(Supplier, pk=self.kwargs['pk'])
        context['supplier'] = supplier
        return context

    def get_queryset(self):
        supplier = get_object_or_404(Supplier, pk=self.kwargs['pk'])
        queryset = PurchaseOrder.objects.filter(supplier=supplier)
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(id=query)
        return queryset

class SupplierProductsListView(LoginRequiredMixin,RoleRequiredMixin, ListView):
    model = Product
    template_name = 'listeproduitfournisseur.html'
    context_object_name = 'products'
    paginate_by = 7
    required_roles = ['Admin', 'Employé']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm(self.request.GET)
        supplier = get_object_or_404(Supplier, pk=self.kwargs['pk'])
        context['supplier'] = supplier
        return context

    def get_queryset(self):
        supplier = get_object_or_404(Supplier, pk=self.kwargs['pk'])
        queryset = Product.objects.filter(suppliers__in=[supplier])
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(id=query)
        return queryset


class AddProductView(LoginRequiredMixin,RoleRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'ajouterproduit.html'
    success_url = reverse_lazy('product-list')
    required_roles = ['Admin', 'Employé']


class ProductListView(LoginRequiredMixin,RoleRequiredMixin, ListView):
    model = Product
    template_name = 'listeproduit.html'  # replace with your template
    context_object_name = 'products'
    paginate_by = 7
    form_class = FilterForm
    required_roles = ['Admin', 'Employé']

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


class ProductDetailView(LoginRequiredMixin,RoleRequiredMixin,DetailView):
    model = Product
    template_name = 'detaillproduit.html'
    context_object_name = 'product'
    required_roles = ['Admin', 'Employé']

class AccountListView(LoginRequiredMixin,RoleRequiredMixin, ListView):
    model = Account
    template_name = 'listecompte.html'
    context_object_name = 'accounts'
    paginate_by = 7
    form_class = FilterForm
    required_roles = ['Admin']

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




class PurchaseOrderListView(LoginRequiredMixin,RoleRequiredMixin, ListView):
    model = PurchaseOrder
    template_name = 'listecommande.html'
    context_object_name = 'purchase_orders'
    paginate_by = 7
    form_class = FilterForm
    required_roles = ['Admin', 'Employé']

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


class SaleListView(LoginRequiredMixin,RoleRequiredMixin, ListView):
    model = Sale
    template_name = 'listevente.html'
    context_object_name = 'sales'
    paginate_by = 7
    form_class = FilterForm
    required_roles = ['Admin', 'Employé']

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


class RepairListView(LoginRequiredMixin,RoleRequiredMixin, ListView):
    model = Repair
    template_name = 'listereparation.html'
    context_object_name = 'repairs'
    paginate_by = 7
    form_class = FilterForm
    required_roles = ['Admin', 'Réparateur']

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


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashbord.html'


class AddAccountView(LoginRequiredMixin,RoleRequiredMixin, CreateView):
    model = Account
    form_class = AccountRegistrationForm
    template_name = 'ajoutercompte.html'
    success_url = reverse_lazy('account-list')
    required_roles = ['Admin']



class AccountUpdateView(LoginRequiredMixin,RoleRequiredMixin, PasswordChangeView):
    model = Account
    form_class = CustomSetPasswordForm
    template_name = 'modifiercompte.html'
    success_url = reverse_lazy('account-list')
    required_roles = ['Admin']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = Account.objects.get(pk=self.kwargs['pk'])
        return kwargs




class AccountDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Account
    template_name = 'supprimercompte.html'
    success_url = reverse_lazy('account-list')
    required_roles = ['Admin']




class AddEmployeeView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'ajouteremploye.html'
    success_url = reverse_lazy('employee-list')
    required_roles = ['Admin']




class EmployeeListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Employee
    template_name = 'listeemploye.html'
    context_object_name = 'employees'
    paginate_by = 7
    form_class = FilterForm
    required_roles = ['Admin']

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




class EmployeeUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'modifieremploye.html'
    success_url = reverse_lazy('employee-list')
    required_roles = ['Admin']




class EmployeeDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Employee
    template_name = 'supprimeremploye.html'
    success_url = reverse_lazy('employee-list')
    required_roles = ['Admin']




class ProductUpdateView(LoginRequiredMixin,RoleRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'modifierproduit.html'
    success_url = reverse_lazy('product-list')
    required_roles = ['Admin', 'Employé']


class ProductDeleteView(LoginRequiredMixin,RoleRequiredMixin, DeleteView):
    model = Product
    template_name = 'supprimerproduit.html'
    success_url = reverse_lazy('product-list')
    required_roles = ['Admin', 'Employé']


class AddCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'cat.html'
    success_url = reverse_lazy('add-product')



class AddSaleView(LoginRequiredMixin,RoleRequiredMixin, CreateView):
    model = Sale
    template_name = 'ajoutervente.html'
    form_class = SaleForm
    required_roles = ['Admin', 'Employé']

    def form_valid(self, form):
        self.object = form.save()
        return redirect('update-sale', pk=self.object.pk)

    def get_success_url(self):
        return reverse_lazy('update-sale', kwargs={'pk': self.object.pk})


class SaleUpdateView(LoginRequiredMixin,RoleRequiredMixin, FormView):
    template_name = 'articlevente.html'
    form_class = SaleItemFormSet
    required_roles = ['Admin', 'Employé']

    def get_success_url(self):
        return reverse_lazy('sale-detail', kwargs={'pk': self.sale.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.sale = Sale.objects.get(pk=self.kwargs['pk'])
        kwargs['instance'] = self.sale
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


class SaleCancelView(LoginRequiredMixin,RoleRequiredMixin, DeleteView):
    model = Sale
    template_name = 'supprimervente.html'
    success_url = reverse_lazy('sale-list')
    required_roles = ['Admin', 'Employé']

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete_sale(
            update_product_quantity=True)  # Call the delete_sale method with update_product_quantity=True
        return super().delete(request, *args, **kwargs)


class SaleDetailView(LoginRequiredMixin,RoleRequiredMixin, DetailView):
    model = Sale
    template_name = 'detaillvente.html'
    context_object_name = 'sale'
    required_roles = ['Admin', 'Employé']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sale_items = SaleItem.objects.filter(sale=self.object)
        context['sale_items_exist'] = sale_items.exists()  # Check if there are any sale items
        # Calculate the total for each item
        item_totals = [item.sale_price * item.quantity for item in sale_items]
        # Calculate the total for the sale
        sale_total = sum(item_totals)
        context['sale_items'] = zip(sale_items, item_totals)  # Pass both the items and their totals
        context['sale_total'] = sale_total
        return context


class ProductInitialSellingPriceView(LoginRequiredMixin,RoleRequiredMixin, View):
    required_roles = ['Admin', 'Employé']
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            product = Product.objects.get(pk=pk)
            return JsonResponse({'initial_selling_price': product.initial_selling_price})
        except Product.DoesNotExist:
            raise Http404("Product does not exist")


class AddPurchaseOrderView(LoginRequiredMixin,RoleRequiredMixin, CreateView):
    model = PurchaseOrder
    template_name = 'ajoutercommande.html'
    form_class = PurchaseOrderForm
    success_url = reverse_lazy('purchase-order-list')
    required_roles = ['Admin', 'Employé']

    def form_valid(self, form):
        self.object = form.save()
        return redirect('update-purchase-order', pk=self.object.pk)

    def get_success_url(self):
        return reverse_lazy('update-purchase-order', kwargs={'pk': self.object.pk})


class PurchaseOrderUpdateView(LoginRequiredMixin,RoleRequiredMixin, FormView):
    template_name = 'articlecommande.html'
    form_class = PurchaseOrderItemFormSet
    required_roles = ['Admin', 'Employé']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.purchase_order
        kwargs['queryset'] = PurchaseOrderItem.objects.filter(purchase_order=self.purchase_order)
        kwargs['form_kwargs'] = {'purchase_order': self.purchase_order}  # Pass the PurchaseOrder instance to the form
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

    def get_success_url(self):
        return reverse_lazy('purchase-order-detail', kwargs={'pk': self.purchase_order.pk})

    def post(self, request, *args, **kwargs):
        self.purchase_order = PurchaseOrder.objects.get(pk=self.kwargs['pk'])
        if self.purchase_order.delivery_date:  # replace with your actual condition
            # Display an error message in french and redirect to the purchase order detail view
            messages.error(self.request, "Vous ne pouvez pas modifier une commande déjà livrée.")
            return redirect('purchase-order-detail',
                            pk=self.purchase_order.pk)  # replace 'purchase-order-detail' with your actual detail
            # view name
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.purchase_order = PurchaseOrder.objects.get(pk=self.kwargs['pk'])
        if self.purchase_order.delivery_date:  # replace with your actual condition
            messages.error(self.request, "Vous ne pouvez pas modifier une commande déjà livrée.")
            return redirect('purchase-order-detail',
                            pk=self.purchase_order.pk)  # replace 'purchase-order-detail' with your actual detail
            # view name
        return super().get(request, *args, **kwargs)


class PurchaseOrderDeleteView(LoginRequiredMixin,RoleRequiredMixin, DeleteView):
    model = PurchaseOrder
    template_name = 'supprimercommande.html'
    success_url = reverse_lazy('purchase-order-list')
    required_roles = ['Admin', 'Employé']

class PurchaseOrderDetailView(LoginRequiredMixin, DetailView):
    model = PurchaseOrder
    template_name = 'detaillcommande.html'
    context_object_name = 'purchase_order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        delivery_date = self.object.delivery_date
        purchase_order_items = PurchaseOrderItem.objects.filter(purchase_order=self.object)
        context['purchase_order_items_exist'] = purchase_order_items.exists()  # Check if there are any purchase order items
        if delivery_date:
            # Calculate the total for each item
            item_totals = [item.purchase_price * item.quantity for item in purchase_order_items]
            # Calculate the total for the purchase order
            purchase_order_total = sum(item_totals)
        else:
            item_totals = [0 for item in purchase_order_items]
            purchase_order_total = None

        context['purchase_order_items'] = zip(purchase_order_items, item_totals)  # Pass both the items and their totals
        context['purchase_order_total'] = purchase_order_total
        return context


# class ProductInitialPurchasePriceView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         pk = kwargs.get('pk')
#         try:
#             product = Product.objects.get(pk=pk)
#             return JsonResponse({'initial_buying_price': product.initial_buying_price})
#         except Product.DoesNotExist:
#             raise Http404("Product does not exist")

class PurchaseOrderDeliverView(LoginRequiredMixin,RoleRequiredMixin, FormView):
    template_name = 'prix.html'  # replace with your actual template
    form_class = PurchaseOrderItemDeliveredFormSet
    required_roles = ['Admin', 'Employé']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.purchase_order = get_object_or_404(PurchaseOrder, id=self.kwargs['pk'])
        kwargs['instance'] = self.purchase_order
        return kwargs

    def form_valid(self, form):
        instances = form.save()
        for instance in instances:
            instance.product.quantity += instance.quantity  # Increase the product quantity
            instance.product.save()
        self.purchase_order.delivery_date = timezone.now()
        self.purchase_order.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        self.purchase_order = get_object_or_404(PurchaseOrder, id=self.kwargs['pk'])
        if self.purchase_order.delivery_date:
            messages.error(request, "La commande est déjà livrée.")
            return redirect('purchase-order-detail', pk=self.purchase_order.pk)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.purchase_order = get_object_or_404(PurchaseOrder, id=self.kwargs['pk'])
        if self.purchase_order.delivery_date:
            messages.error(request, "La commande est déjà livrée.")
            return redirect('purchase-order-detail', pk=self.purchase_order.pk)
        return super().post(request, *args, **kwargs)
    def get_success_url(self):
        return reverse_lazy('purchase-order-detail', kwargs={'pk': self.purchase_order.pk})


class AddRepairView(LoginRequiredMixin,RoleRequiredMixin, CreateView):
    model = Repair
    template_name = 'ajouterreparation.html'
    form_class = RepairForm
    required_roles = ['Admin', 'Réparateur']
    def get_success_url(self):
        return reverse('repair-detail', kwargs={'pk': self.object.pk})


class RepairDetailView(LoginRequiredMixin,RoleRequiredMixin, DetailView):
    model = Repair
    template_name = 'detaillreparation.html'
    context_object_name = 'repair'
    required_roles = ['Admin', 'Réparateur']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        left_to_pay = self.object.repair_price - self.object.prepayment
        context['left_to_pay'] = left_to_pay
        return context


class RepairUpdateView(LoginRequiredMixin,RoleRequiredMixin, UpdateView):
    model = Repair
    form_class = RepairForm
    template_name = 'modifierreparation.html'
    required_roles = ['Admin', 'Réparateur']
    def form_valid(self, form):
        # Check if any data has changed and the repair is done
        if form.has_changed() and self.object.state == 'Réparation terminée':
            self.object.state = 'En cours'
            self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('repair-detail', kwargs={'pk': self.object.pk})


class RepairDeleteView(LoginRequiredMixin,RoleRequiredMixin, DeleteView):
    model = Repair
    template_name = 'supprimerreparation.html'
    success_url = reverse_lazy('repair-list')
    required_roles = ['Admin', 'Réparateur']

class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'login'



class RepairFinishView(LoginRequiredMixin,RoleRequiredMixin, View):
    required_roles = ['Admin', 'Réparateur']
    def post(self, request, *args, **kwargs):
        repair = get_object_or_404(Repair, pk=kwargs['pk'])

        # Check if the repair is already done
        if repair.state == 'Réparation terminée':
            # Display an error in french message and redirect to the repair detail view
            messages.error(request, "La réparation est déjà terminée.")
            return redirect('repair-detail', pk=repair.pk)

        # Update the state of the repair and the product
        repair.state = 'Réparation terminée'
        repair.save()

        hardware = repair.hardware
        hardware.state = 'Réparation terminée'
        hardware.save()
        # Display a success message in french and redirect to the repair detail view
        messages.success(request, "La réparation a été terminée avec succès.")
        return redirect('repair-detail', pk=repair.pk)

class RepairPayView(LoginRequiredMixin,RoleRequiredMixin, View):
    required_roles = ['Admin', 'Réparateur']
    def post(self, request, *args, **kwargs):
        repair = get_object_or_404(Repair, pk=kwargs['pk'])

        # Check if the repair is done
        if repair.state != 'Réparation terminée':
            # Display an error message in french and redirect to the repair detail view
            messages.error(request, "La réparation n'est pas encore terminée.")
            return redirect('repair-detail', pk=repair.pk)


        # Display a success message in french and redirect to the repair detail view and change the state to paid and set payment date
        repair.state = 'Réparation payée'
        repair.delivery_date=timezone.now()
        repair.save()
        messages.success(request, "La réparation a été payée avec succès.")
        return redirect('repair-detail', pk=repair.pk)


class SaleInvoiceView(LoginRequiredMixin,RoleRequiredMixin,View):
    required_roles = ['Admin', 'Employé']
    def get(self, request, *args, **kwargs):
        sale = get_object_or_404(Sale, id=self.kwargs['pk'])
        sale_items = SaleItem.objects.filter(sale=sale)
        if not sale.client:
            messages.error(request, "La vente n'a pas de client. Vous ne pouvez pas imprimer la facture.")
        if (not sale_items.exists()):
            messages.error(request, "La vente ne contient aucun article. Vous ne pouvez pas imprimer la facture.")
        if not(sale.client and sale_items.exists()):
            return redirect('sale-detail', pk=sale.pk)
        # Calculate the total for each item
        item_totals = [item.sale_price * item.quantity for item in sale_items]
        # Calculate the total for the sale
        sale_total = sum(item_totals)

        data = {
            'sale': sale,
            # Check if there are any sale items
            'sale_items_exist': sale_items.exists(),
            'sale_items': zip(sale_items, item_totals),
            'sale_total': sale_total,
            # include any other data you need in the template
        }

        # Rendered html content as a string
        html_string = render_to_string('facturevente.html', data)

        # Create a WeasyPrint HTML object and write it to PDF
        html = HTML(string=html_string)
        pdf_content = BytesIO()
        html.write_pdf(target=pdf_content)

        # Rewind the BytesIO object to the start
        pdf_content.seek(0)

        # Create a Django response object, and specify content_type as pdf
        response = FileResponse(pdf_content, content_type='application/pdf')

        # Otherwise, set it to "inline"
        response['Content-Disposition'] = 'inline'

        return response


class PurchaseOrderPrintView(LoginRequiredMixin, RoleRequiredMixin, View):
    required_roles = ['Admin', 'Employé']
    def get(self, request, *args, **kwargs):
        purchase_order = get_object_or_404(PurchaseOrder, id=self.kwargs['pk'])
        purchase_order_items = PurchaseOrderItem.objects.filter(purchase_order=purchase_order)
        if not purchase_order.supplier:
            messages.error(request, "La commande n'a pas de fournisseur. Vous ne pouvez pas imprimer la commande.")
        if (not purchase_order_items.exists()):
            messages.error(request, "La commande ne contient aucun article. Vous ne pouvez pas imprimer la facture.")
        if not (purchase_order.supplier and purchase_order_items.exists()):
            return redirect('purchase-order-detail', pk=purchase_order.pk)


        data = {
            'purchase_order': purchase_order,
            'purchase_order_items': purchase_order_items,
            # Check if there are any purchase order items
            'purchase_order_items_exist': purchase_order_items.exists(),
            # include any other data you need in the template
        }

        # Rendered html content as a string
        html_string = render_to_string('commande_pdf.html', data)

        # Create a WeasyPrint HTML object and write it to PDF
        html = HTML(string=html_string)
        pdf_content = BytesIO()
        html.write_pdf(target=pdf_content)

        # Rewind the BytesIO object to the start
        pdf_content.seek(0)

        # Create a Django response object, and specify content_type as pdf
        response = FileResponse(pdf_content, content_type='application/pdf')

        # Otherwise, set it to "inline"
        response['Content-Disposition'] = 'inline'

        return response


class RepairInvoiceView(LoginRequiredMixin,RoleRequiredMixin, View):
    required_roles = ['Admin', 'Réparateur']
    def get(self, request, *args, **kwargs):
        repair = get_object_or_404(Repair, id=self.kwargs['pk'])
        left_to_pay = repair.repair_price - repair.prepayment

        # Check if the repair is done
        if repair.state == 'En cours':
            messages.error(request, "La réparation n'est pas encore terminée. Vous ne pouvez pas imprimer la facture.")
        if not repair.client:
            messages.error(request, "La réparation n'a pas de client. Vous ne pouvez pas imprimer la facture.")
        if not (repair.client and repair.state != 'En cours'):
            return redirect('repair-detail', pk=repair.pk)

        data = {
            'repair': repair,
            'left_to_pay': left_to_pay,
            # include any other data you need in the template
        }


        # Rendered html content as a string
        html_string = render_to_string('facturereparation.html', data)

        # Create a WeasyPrint HTML object and write it to PDF
        html = HTML(string=html_string)
        pdf_content = BytesIO()
        html.write_pdf(target=pdf_content)

        # Rewind the BytesIO object to the start
        pdf_content.seek(0)

        # Create a Django response object, and specify content_type as pdf
        response = FileResponse(pdf_content, content_type='application/pdf')

        # Otherwise, set it to "inline"
        response['Content-Disposition'] = 'inline'

        return response


class HardwareToRepairListView(LoginRequiredMixin,RoleRequiredMixin, ListView):
    model = HardwareToRepair
    template_name = 'listemat.html'  # replace with your actual template
    context_object_name = 'hardwares'
    paginate_by = 7
    form_class = FilterForm
    required_roles = ['Admin', 'Réparateur']

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


class AddHardwareToRepairView(LoginRequiredMixin,RoleRequiredMixin, CreateView):
    model = HardwareToRepair
    form_class = HardwareToRepairForm
    template_name = 'ajoutermat.html'  # replace with your actual template
    required_roles = ['Admin', 'Réparateur']

    def get_success_url(self):
        return reverse_lazy('hardware-detail', kwargs={'pk': self.object.pk})  # replace with your actual url name


class HardwareToRepairUpdateView(LoginRequiredMixin,RoleRequiredMixin, UpdateView):
    model = HardwareToRepair
    form_class = HardwareToRepairForm
    template_name = 'modifiermat.html'  # replace with your actual template
    required_roles = ['Admin', 'Réparateur']
    def get_success_url(self):
        return reverse_lazy('hardware-detail', kwargs={'pk': self.object.pk})  # replace with your actual url name


class HardwareToRepairDeleteView(LoginRequiredMixin,RoleRequiredMixin, DeleteView):
    model = HardwareToRepair
    template_name = 'supprimermat.html'  # replace with your actual template
    success_url = reverse_lazy('hardware-list')  # replace with your actual url name
    required_roles = ['Admin', 'Réparateur']

class HardwareToRepairDetailView(LoginRequiredMixin,RoleRequiredMixin, DetailView):
    model = HardwareToRepair
    template_name = 'detaillmat.html'  # replace with your actual template
    context_object_name = 'hardware'  # replace with your actual context object name
    required_roles = ['Admin', 'Réparateur']

class RepairReceiptView(LoginRequiredMixin,RoleRequiredMixin, View):
    required_roles = ['Admin', 'Réparateur']
    def get(self, request, *args, **kwargs):
        repair = get_object_or_404(Repair, id=self.kwargs['pk'])
        left_to_pay = repair.repair_price - repair.prepayment

        # check if the hardware is delivered , if it is then redirect to repair details page with error message
        if repair.delivery_date:
            messages.error(request, "Le matériel est déja livré . Vous ne pouvez pas imprimer le bon de réparation.")
            return redirect('repair-detail', pk=repair.pk)

        data = {
            'repair': repair,
            'left_to_pay': left_to_pay,
            # include any other data you need in the template
        }

        # Rendered html content as a string
        html_string = render_to_string('bonreparation.html', data)

        # Create a WeasyPrint HTML object and write it to PDF
        html = HTML(string=html_string)
        pdf_content = BytesIO()
        html.write_pdf(target=pdf_content)

        # Rewind the BytesIO object to the start
        pdf_content.seek(0)

        # Create a Django response object, and specify content_type as pdf
        response = FileResponse(pdf_content, content_type='application/pdf')

        # Otherwise, set it to "inline"
        response['Content-Disposition'] = 'inline'

        return response
