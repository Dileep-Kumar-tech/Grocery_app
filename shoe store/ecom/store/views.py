from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Products,Carts,profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signin')

        if profile.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signin')

        if profile.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('signin')

        hashed_password = make_password(password)
        profile.objects.create(username=username, email=email, password=hashed_password)
        messages.success(request, "signin successful! Please login.")
        return redirect('login')

    return render(request, 'signin.html')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            customer = profile.objects.get(username=username)
            if check_password(password, customer.password):
                request.session['customer_id'] = customer.id
                messages.success(request, "Login successful!")
                return redirect('home')
            else:
                messages.error(request, "Invalid password!")
        except profile.DoesNotExist:
            messages.error(request, "User not found!")

        return redirect('login')

    return render(request, 'login.html')


def home(request):
    if 'customer_id' not in request.session:
        return redirect('login')
    products = Products.objects.all()
    return render(request, 'home.html', {'products': products})


def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

# Add to Cart
def add_to_cart(request, product_id):
    if 'customer_id' not in request.session:
        return redirect('login')
    try:
        customer = profile.objects.get(id=request.session['customer_id'])
    except profile.DoesNotExist:
        return redirect('login')
    product = Products.objects.get(id=product_id)
    cart_item, created = Carts.objects.get_or_create(customer=customer, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('home')

# cart details
def cart(request):
    if 'customer_id' not in request.session:
        return redirect('login')
    try:
        customer_id = profile.objects.get(id=request.session['customer_id'])
    except profile.DoesNotExist:
        return redirect('login')
    cart_items = Carts.objects.filter(customer_id=customer_id)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


# quantity increase or decrease
def update_cart(request, cart_item_id, action):
    cart_item = get_object_or_404(Carts, id=cart_item_id)
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()
    return redirect('cart')


# Remove from Cart
def remove_from_cart(request, item_id):
    cart_item = Carts.objects.get(id=item_id)
    cart_item.delete()
    messages.success(request, "Item removed from cart!")
    return redirect('cart')







