from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.urls import reverse_lazy, reverse
from .forms import *
from django.db.models import Q


class custmoervisit(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user:
                customer_obj = Customer.objects.get(user=request.user)
                cart_obj.customer = customer_obj
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)


def index(request):
    return render(request, 'blog/home.html')

def OurBrunches(request):
    return render(request, 'blog/OurBrunches.html')



def customerservice(request):
    return render(request, 'blog/servicePoilcy.html')

def confirmations(request):
    return render(request, 'blog/confirmation.html')








class good(custmoervisit, TemplateView):
    template_name = "blog/good.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = goods.objects.all()
        return context


class AllProductsView(custmoervisit, TemplateView):
    template_name = "blog/allproducts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context


class AddToCart(custmoervisit, TemplateView):
    template_name = "blog/cart.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = goods.objects.get(id=product_id)

        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)


        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)
            cart = Cart.objects.get(id=cart_id)
            context['cart'] = cart
            # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.price
                cartproduct.save()
                cart_obj.total += product_obj.price
                cart_obj.save()
                context['cart'] = cart
            # new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, price=product_obj.price, quantity=1, subtotal=product_obj.price)
                cart_obj.total += product_obj.price
                cart_obj.save()
                context['cart'] = cart
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, price=product_obj.price, quantity=1, subtotal=product_obj.price)
            cart_obj.total += product_obj.price
            cart_obj.save()
            cart_id = self.request.session.get("cart_id", None)
            cart = Cart.objects.get(id=cart_id)
            context['cart'] = cart
        return context

class MyCartView(custmoervisit, TemplateView):
    template_name = "blog/cart.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context


class ManageCartView(custmoervisit, View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.price
            cp_obj.save()
            cart_obj.total += cp_obj.price
            cart_obj.save()
        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.price
            cp_obj.save()
            cart_obj.total -= cp_obj.price
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("blog:cart")


class CheckoutView(custmoervisit, CreateView):
    template_name = "blog/checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("blog:confirmation")

    # when never user request this method will be excuted
    def dispatch(self, request, *args, **kwargs):
        # this condition if user logged in or not
        # secoend condtion if user have customer
        if request.user.is_authenticated and request.user.customer:
            # if both correct will go
            pass
        else:
            return redirect("/login/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"
            del self.request.session['cart_id']
        else:
            return redirect("blog:good")
        return super().form_valid(form)


class CustomerRegistrationView(CreateView):
    template_name = "blog/customerregistration.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("blog:customerlogin")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class CustomerlogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("blog:home")


# same as register
class CustomerloginView(FormView):
    template_name = "blog/customerlogin.html"
    form_class = customerloginForm
    success_url = reverse_lazy("blog:home")

    # form_valid method is a type of post method and is available in createview formview and updateview
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]

        user = authenticate(username=uname, password=pword)
        if user is not None and Customer.objects.filter(user=user).exists():
            login(self.request, user)
        else:
            return render(self.request, self.template_name,
                          {"form": self.form_class, "error": "Invalid Username or Password"})

        return super().form_valid(form)

    # self as argument
    # return to the next page
    # if it is  not will return to the home
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


# here customer must login
# to check the log in the same as checking view
class CustomerProfileView(TemplateView):
    template_name = "blog/customerprofile.html"

    # method to log in it much should be valid to go the next page
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        # which defined customer and then add to the html to see the value
        context['customer'] = customer
        # here means we need such type of orders whose card customer is etc
        orders = Order.objects.filter(cart__customer=customer).order_by("-id")
        context["orders"] = orders
        return context

class CustomerOrderDetailView(DetailView):
    template_name = "blog/customerorderdetail.html"
    model = Order
    #optinal attrbuite
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            if request.user.customer != order.cart.customer:
                return redirect("customerprofile")
        else:
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)


class SearchView(TemplateView):
    template_name = "blog/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = goods.objects.filter(
            Q(name__icontains=kw))
        print(results)
        context["results"] = results
        return context

# admin pages
class AdminLoginView(FormView):
    template_name = "adminpages/adminlogin.html"
    form_class = customerloginForm
    success_url = reverse_lazy("blog:adminhome")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)


class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/adminhome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pendingorders"] = Order.objects.filter(
            order_status="Order Received").order_by("-id")
        return context


class AdminOrderDetailView(AdminRequiredMixin, DetailView):
    template_name = "adminpages/adminorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        return context


class AdminOrderListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminorderlist.html"
    queryset = Order.objects.all().order_by("-id")
    context_object_name = "allorders"


class AdminOrderStatuChangeView(AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order_obj = Order.objects.get(id=order_id)
        new_status = request.POST.get("status")
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy("blog:adminorderdetail", kwargs={"pk": order_id}))


class AdminProductListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminproductlist.html"
    queryset = goods.objects.all().order_by("-id")
    context_object_name = "allproducts"


class AdminProductCreateView(AdminRequiredMixin, CreateView):
    template_name = "adminpages/adminproductcreate.html"
    form_class = goodForm
    success_url = reverse_lazy("blog:adminproductlist")

    def form_valid(self, form):
        p = form.save()
        return super().form_valid(form)

