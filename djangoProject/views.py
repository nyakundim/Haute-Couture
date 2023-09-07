from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Product, Feedback, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import DetailView, View
from django.utils import timezone


def index(request):
    if 'user' in request.session:
        current_user = request.session['user']
        param = {'current_user': current_user}
        return render(request, 'index.html', param)
    else:
        return render(request, 'index.html')


def handlesignup(request):
    if request.method == "POST":
        name = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if User.objects.filter(username=name).count() > 0:
            return HttpResponse('Username already exists.')
        else:
            myuser = User.objects.create_user(name, email, password)
            myuser.save()
            return redirect('home')


def handlelogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['user'] = username
            return redirect('home')

        else:
            return HttpResponse('invalid credentials')


def userlogout(request):
    if request.method == "POST":
        del request.session['user']
        logout(request)
    return redirect('home')


def feedback(request):
    if request.method == "POST":
        feedback = request.POST.get('feed')

        query = Feedback(feedback=feedback)
        query.save()
        return redirect('home')


def allproducts(request):
    data = Product.objects.all()
    context = {
        'data': data
    }
    return render(request, "product.html", context)


# def price_up(request):
#     data = Product.objects.order_by('value')
#     context = {
#         'data': data
#     }
#     return render(request, "product.html", context)
#
#
# def price_down(request):
#     data = Product.objects.order_by('-value')
#     context = {
#         'data': data
#     }
#     return render(request, "product.html", context)


def product(request):
    data = Product.objects.filter(category__iexact='Athletic')
    context = {
        'data': data
    }
    return render(request, "product.html", context)


def casual(request):
    data = Product.objects.filter(category__iexact='Casual')
    context = {
        'data': data
    }
    return render(request, "product.html", context)


def streetwear(request):
    data = Product.objects.filter(category__iexact='Streetwear')
    context = {
        'data': data
    }
    return render(request, "product.html", context)


class Productdetail(DetailView):
    model = Product
    template_name = "product_detail.html"


# class Casualdetail(DetailView):
#     model = Casual
#     template_name = "casual_detail.html"
#
#
# class Streetweardetail(DetailView):
#     model = Streetwear
#     template_name = "street_detail.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("/")


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Added quantity Item")
            return redirect("order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "Item added to your cart")
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to your cart")
        return redirect("order-summary")


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.delete()
            messages.info(request, "Item \"" + order_item.item.name + "\" remove from your cart")
            return redirect("order-summary")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("product", pk=pk)
    else:

        messages.info(request, "You do not have an Order")
        return redirect("product", pk=pk)


@login_required
def reduce_quantity_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, "Item quantity was updated")
            return redirect("order-summary")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("order-summary")
    else:

        messages.info(request, "You do not have an Order")
        return redirect("order-summary")


def filter(request):
    if request.method == "POST":
        category = request.POST.get("category")
        sort = request.POST.get("sort")

        if category == "Athletic" and sort == "Low to High":
            data = Product.objects.filter(category__iexact='Athletic').order_by('value')
            context = {
                'data': data
            }
            return render(request, "product.html", context)

        elif category == "Athletic":
            data = Product.objects.filter(category__iexact='Athletic').order_by('-value')
            context = {
                'data': data
            }
            return render(request, "product.html", context)

        elif category == "Casual" and sort == "Low to High":
            data = Product.objects.filter(category__iexact='Casual').order_by('value')
            context = {
                'data': data
            }
            return render(request, "product.html", context)

        elif category == "Casual":
            data = Product.objects.filter(category__iexact='Casual').order_by('-value')
            context = {
                'data': data
            }
            return render(request, "product.html", context)

        elif category == "Streetwear" and sort == "Low to High":
            data = Product.objects.filter(category__iexact='Streetwear').order_by('value')
            context = {
                'data': data
            }
            return render(request, "product.html", context)

        elif category == "Streetwear":
            data = Product.objects.filter(category__iexact='Streetwear').order_by('-value')
            context = {
                'data': data
            }
            return render(request, "product.html", context)

        elif category == "All products" and sort == "Low to High":
            data = Product.objects.all().order_by('value')
            context = {
                'data': data
            }
            return render(request, "product.html", context)

        elif category == "All products":
            data = Product.objects.all().order_by('-value')
            context = {
                'data': data
            }
            return render(request, "product.html", context)
