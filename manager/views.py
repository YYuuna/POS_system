from io import BytesIO

from django.template.loader import render_to_string
from django.utils import timezone

from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.contrib import messages
from django.http import JsonResponse, Http404, FileResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, TemplateView, DetailView
from django.urls import reverse_lazy, reverse
from weasyprint import HTML

from .models import Client, Supplier, Product, Account, Employee, PurchaseOrder, Sale, Repair, Category, SaleItem, \
    PurchaseOrderItem, HardwareToRepair
from .forms import ClientForm, UserLoginForm, FilterForm, SupplierForm, ProductForm, AccountRegistrationForm, \
    EmployeeForm, CategoryForm, SaleForm, SaleItemFormSet, SaleItemForm, PurchaseOrderForm, PurchaseOrderItemFormSet, \
    PurchaseOrderItemForm, RepairForm, CustomSetPasswordForm, HardwareToRepairForm


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
    paginate_by = 7
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
    template_name = 'modifierfournisseur.html'
    success_url = reverse_lazy('supplier-list')


class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'supprimerfournisseur.html'
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
    paginate_by = 7
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
    paginate_by = 7
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
    paginate_by = 7
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
    paginate_by = 7
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
    paginate_by = 7
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


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashbord.html'


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
    form_class = CustomSetPasswordForm
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
    paginate_by = 7
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
    form_class = SaleItemFormSet

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


class SaleCancelView(LoginRequiredMixin, DeleteView):
    model = Sale
    template_name = 'supprimervente.html'
    success_url = reverse_lazy('sale-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete_sale(
            update_product_quantity=True)  # Call the delete_sale method with update_product_quantity=True
        return super().delete(request, *args, **kwargs)


class SaleDetailView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = 'detaillvente.html'
    context_object_name = 'sale'

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


class ProductInitialSellingPriceView(LoginRequiredMixin, View):
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
    form_class = PurchaseOrderItemFormSet

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.purchase_order
        kwargs['queryset'] = PurchaseOrderItem.objects.filter(purchase_order=self.purchase_order)
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


class PurchaseOrderDeleteView(LoginRequiredMixin, DeleteView):
    model = PurchaseOrder
    template_name = 'supprimercommande.html'
    success_url = reverse_lazy('purchase-order-list')


class PurchaseOrderDetailView(LoginRequiredMixin, DetailView):
    model = PurchaseOrder
    template_name = 'detaillcommande.html'
    context_object_name = 'purchase_order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchase_order_items = PurchaseOrderItem.objects.filter(purchase_order=self.object)
        context[
            'purchase_order_items_exist'] = purchase_order_items.exists()  # Check if there are any purchase order items
        # Calculate the total for each item
        item_totals = [item.purchase_price * item.quantity for item in purchase_order_items]
        # Calculate the total for the purchase order
        purchase_order_total = sum(item_totals)
        context['purchase_order_items'] = zip(purchase_order_items, item_totals)  # Pass both the items and their totals
        context['purchase_order_total'] = purchase_order_total
        return context


class ProductInitialPurchasePriceView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            product = Product.objects.get(pk=pk)
            return JsonResponse({'initial_buying_price': product.initial_buying_price})
        except Product.DoesNotExist:
            raise Http404("Product does not exist")


class AddRepairView(LoginRequiredMixin, CreateView):
    model = Repair
    template_name = 'ajouterreparation.html'
    form_class = RepairForm

    def get_success_url(self):
        return reverse('repair-detail', kwargs={'pk': self.object.pk})


class RepairDetailView(LoginRequiredMixin, DetailView):
    model = Repair
    template_name = 'detaillreparation.html'
    context_object_name = 'repair'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        left_to_pay = self.object.repair_price - self.object.prepayment
        context['left_to_pay'] = left_to_pay
        return context


class RepairUpdateView(LoginRequiredMixin, UpdateView):
    model = Repair
    form_class = RepairForm
    template_name = 'modifierreparation.html'

    def form_valid(self, form):
        # Check if any data has changed and the repair is done
        if form.has_changed() and self.object.state == 'Réparation terminée':
            self.object.state = 'En cours'
            self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('repair-detail', kwargs={'pk': self.object.pk})


class RepairDeleteView(LoginRequiredMixin, DeleteView):
    model = Repair
    template_name = 'supprimerreparation.html'
    success_url = reverse_lazy('repair-list')


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'login'


class PurchaseOrderDeliverView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = get_object_or_404(PurchaseOrder, pk=kwargs['pk'])

        # Check if the order is already delivered
        if order.delivery_date is not None:
            # Display an error message in french and redirect to the purchase order detail view
            messages.error(request, "La commande est déjà livrée.")
            return redirect('purchase-order-detail', pk=order.pk)

        order.delivery_date = timezone.now()
        order.save()

        for item in order.purchaseorderitem_set.all():
            product = item.product
            product.quantity += item.quantity
            product.save()

        # Display a success message in french and redirect to the purchase order detail view
        messages.success(request, "La commande a été livrée avec succès.")
        return redirect('purchase-order-detail', pk=order.pk)


class RepairFinishView(LoginRequiredMixin, View):
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


class SaleInvoiceView(View):
    def get(self, request, *args, **kwargs):
        sale = get_object_or_404(Sale, id=self.kwargs['pk'])
        sale_items = SaleItem.objects.filter(sale=sale)
        if (not sale_items.exists()):
            messages.error(request, "La vente ne contient aucun article. Vous ne pouvez pas imprimer la facture.")
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


class PurchaseOrderInvoiceView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        purchase_order = get_object_or_404(PurchaseOrder, id=self.kwargs['pk'])
        purchase_order_items = PurchaseOrderItem.objects.filter(purchase_order=purchase_order)
        if (not purchase_order_items.exists()):
            messages.error(request, "La commande ne contient aucun article. Vous ne pouvez pas imprimer la facture.")
            return redirect('purchase-order-detail', pk=purchase_order.pk)
        # Calculate the total for each item
        item_totals = [item.purchase_price * item.quantity for item in purchase_order_items]
        # Calculate the total for the purchase order
        purchase_order_total = sum(item_totals)

        data = {
            'purchase_order': purchase_order,
            # Check if there are any purchase order items
            'purchase_order_items_exist': purchase_order_items.exists(),
            'purchase_order_items': zip(purchase_order_items, item_totals),
            'purchase_order_total': purchase_order_total,
            # include any other data you need in the template
        }

        # Rendered html content as a string
        html_string = render_to_string('facturecommande.html', data)

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


class RepairInvoiceView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        repair = get_object_or_404(Repair, id=self.kwargs['pk'])
        left_to_pay = repair.repair_price - repair.prepayment

        # Check if the repair is done
        if repair.state != 'Réparation terminée':
            messages.error(request, "La réparation n'est pas encore terminée. Vous ne pouvez pas imprimer la facture.")
            return redirect('repair-detail', pk=repair.pk)

        data = {
            'repair': repair,
            'left_to_pay': left_to_pay,
            # include any other data you need in the template
        }

        # set the repair delivery date to now if it is not set yet
        if not repair.delivery_date:
            repair.delivery_date = timezone.now()
            repair.save()

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


class HardwareToRepairListView(LoginRequiredMixin, ListView):
    model = HardwareToRepair
    template_name = 'listemat.html'  # replace with your actual template
    context_object_name = 'hardwares'
    paginate_by = 7
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


class AddHardwareToRepairView(LoginRequiredMixin, CreateView):
    model = HardwareToRepair
    form_class = HardwareToRepairForm
    template_name = 'ajoutermat.html'  # replace with your actual template

    def get_success_url(self):
        return reverse_lazy('hardware-detail', pk=self.object.pk)  # replace with your actual url name


class HardwareToRepairUpdateView(LoginRequiredMixin, UpdateView):
    model = HardwareToRepair
    form_class = HardwareToRepairForm
    template_name = 'modifiermat.html'  # replace with your actual template

    def get_success_url(self):
        return reverse_lazy('hardware-detail', pk=self.object.pk)  # replace with your actual url name


class HardwareToRepairDeleteView(LoginRequiredMixin, DeleteView):
    model = HardwareToRepair
    template_name = 'supprimermat.html'  # replace with your actual template
    success_url = reverse_lazy('hardware-list')  # replace with your actual url name


class HardwareToRepairDetailView(LoginRequiredMixin, DetailView):
    model = HardwareToRepair
    template_name = 'detaillmat.html'  # replace with your actual template
    context_object_name = 'hardware'  # replace with your actual context object name


class RepairReceiptView(LoginRequiredMixin, View):
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
