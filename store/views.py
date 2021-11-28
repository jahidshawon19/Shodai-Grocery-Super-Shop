
from django.shortcuts import redirect, render, get_object_or_404
from.models import *
from django.views import View
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages 
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
# Create your views here.

# def homePage(request):
#     return render(request, 'index.html')

class ProductView(View):
    def get(self, request):
        banner_image = get_object_or_404(Banner,id=1)
        grocery_product = Product.objects.filter(category='Grocery')
        rice_product = Product.objects.filter(category='Rice')
        fish_product = Product.objects.filter(category='Fish')
        meat_product = Product.objects.filter(category='Meat')
        vegetables_product = Product.objects.filter(category='Vegetables')
        household_product = Product.objects.filter(category='Household & Clean')
        dairy_product = Product.objects.filter(category='Dairy')
        beverage_product = Product.objects.filter(category='Beverages')
        backery_product = Product.objects.filter(category='Bakery & Snacks')

        context = {
            'grocery_product':grocery_product,
            'rice_product':rice_product,
            'fish_product':fish_product,
            'banner_image':banner_image,
            'mp':meat_product,
            'vp':vegetables_product,
            'hp':household_product,
            'dp':dairy_product,
            'bp':beverage_product,
            'bk':backery_product,


        }
        return render(request, 'index.html', context)


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False 
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        context = {
            'product':product,
            'item_already_in_cart':item_already_in_cart,
            
        }
        return render(request, 'product-detail.html', context)



class  CustomerRegistrationView(View):
    # if user request is get it will just show a blank form
    def get(self, request):
        form = CustomerRegistrationForm()
        context = {
            'form':form,
        }
        return render(request, 'customer-registration.html', context)
    # if user request is post it will save the form and render 
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulation! Your Registration Successfully Completed.Please Login Now.Thank You.')
            form.save()
        context = {
            'form':form,
        }
        return render(request, 'customer-registration.html', context)


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        context = {
            'form':form,
        }
        return render(request, 'profile.html',context)
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            current_user = request.user
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            area = form.cleaned_data['area']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user= current_user, name=name,phone=phone,email=email,address=address,city=city,area=area,zipcode=zipcode)
            reg.save()
            return redirect('address')
        context = {
        'form':form,
        }
        return render(request, 'profile.html', context)


@login_required
def Address(request):
    customer_address = Customer.objects.filter(user=request.user)
    context = {
        'customer_address':customer_address,
    }
    return render(request, 'address.html', context)


@login_required
def cart(request):
    current_user = request.user 
    product_id = request.GET.get('prod_id')
    cart_product = Product.objects.get(id=product_id)
    my_cart = Cart(user=current_user,product=cart_product)
    my_cart.save()
    return redirect ('show-cart')


def display_cart(request):
    if request.user.is_authenticated:
        current_user = request.user 
        my_cart = Cart.objects.filter(user=current_user) # means fetch cart data only for logined user
        amount = 0.0 
        shipping_amount = 10
        total_amount = 0.0 
        my_cart_products = [ p for p in Cart.objects.all() if p.user == current_user]

        if my_cart_products:
            for p in my_cart_products:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount += temp_amount
                total_amount = amount + shipping_amount
       
            context = {
                'my_cart':my_cart,
                'total_amount':total_amount,
                'amount':amount,
            }
            return render (request, 'cart.html', context)
        else:
            return render(request,"emptycart.html")



def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()

        amount = 0.0 
        shipping_amount = 10.0 
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount 
        data = {
            'quantity': c.quantity,
            'amount':amount,
            'total_amount':amount + shipping_amount
            }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()

        amount = 0.0 
        shipping_amount = 10.0 
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount 
            
        data = {
            'quantity': c.quantity,
            'amount':amount,
            'total_amount':amount + shipping_amount
            }
        return JsonResponse(data)



def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()

        amount = 0.0 
        shipping_amount = 10.0 
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount 
 
        data = {
            
            'amount':amount,
            'total_amount':amount + shipping_amount
            }
        return JsonResponse(data)



@login_required
def checkout(request):
    current_user = request.user 
    address = Customer.objects.filter(user=current_user)
    cart_items = Cart.objects.filter(user=current_user)
    amount = 0.0
    shipping_amount = 10.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount 
        total_amount = amount + shipping_amount
    context = {
        'address':address,
        'total_amount':total_amount,
        'cart_items':cart_items,
    }
    return render(request, 'checkout.html', context)


@login_required
def payment_done(request):
    current_user = request.user 
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id = custid)
    cart = Cart.objects.filter(user = current_user)
    for c in cart:
        Order(user=current_user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    
    return redirect('orders')


@login_required
def orders(request):
    order_place = Order.objects.filter(user = request.user)
    context ={
        'order_place':order_place,
    }
    return render(request, 'orders.html', context)