from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, Cart
from .forms import ProductFilterForm
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from .models import Cart, CartItem, Product, Profile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .forms import EditProfileForm
def home_view(request):
    return render(request, 'home.html')
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('products')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('products')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Profile.objects.create(user=user)
            return redirect('products')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('products')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('products')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def product_list_view(request):
    form = ProductFilterForm(request.GET)
    products = Product.objects.all()

    if form.is_valid():
        if form.cleaned_data['min_price']:
            products = products.filter(price__gte=form.cleaned_data['min_price'])
        if form.cleaned_data['max_price']:
            products = products.filter(price__lte=form.cleaned_data['max_price'])
        if form.cleaned_data['brand']:
            products = products.filter(brand=form.cleaned_data['brand'])

    return render(request, 'product_list.html', {'form': form, 'products': products})



@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def cart_view(request):
    cart = Cart.objects.get(user=request.user)
    return render(request, 'cart.html', {'cart': cart})


@login_required
def add_to_cart(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            if product_id is None:
                return JsonResponse({"error": "Missing product_id in request body"}, status=400)
            product = get_object_or_404(Product, id=product_id)
            cart = Cart.objects.get(user=request.user)
            cart.products.add(product)
            return JsonResponse({"message": "Product added to cart successfully."}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def clear_cart(request):
    if request.method == 'GET':
        try:
            cart = Cart.objects.get(user=request.user)
            cart.products.clear()
            return JsonResponse({"message": "Cart cleared successfully."}, status=200)
        except Cart.DoesNotExist:
            return JsonResponse({"error": "Cart does not exist."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)