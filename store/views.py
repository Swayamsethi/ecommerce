from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import User,Products,CartItems
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user_role = request.POST.get('user_type')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        User.objects.create(postal_code=postal_code,city=city,profile_pic=profile_pic,first_name=first_name,last_name=last_name, email=email, password=make_password(password), user_role= user_role, gender=gender)
        messages.success(request, "User registered successfully!")
        return redirect('login')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home') 
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'login.html')

    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

@login_required
def home(request):
    user_role= request.user.user_role
    if user_role == 2:
        products= Products.objects.all()
    elif user_role in [1,3]:
        products= Products.objects.filter(created_by= request.user)
    else:
        products= []
    return render(request, 'home.html', context = {'products': products})

def UserProfile(request):
    user = request.user
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        profile_pic = request.FILES.get('profile_pic')
        postal_code = request.POST.get('postal_code')
        city = request.POST.get('city')

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.gender = gender  
        user.password = password
        user.profile_pic = profile_pic
        user.postal_code = postal_code
        user.city = city

        user.save() 
        return redirect('home')
    return render(request, 'profile.html', {'user': user})

def delete_profile_pic(request):
    user=request.user
    if user.profile_pic == request.user:
        user.delete()
    return redirect('profile')

def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        try:
            Products.objects.create(name=name,price=price, description=description, image=image, created_by= request.user)
            messages.success(request, "Product created successfully!")
            return redirect('home')
        except Exception as e:
            messages.error(request, str(e))
    return render(request, 'createproduct.html')


def update_product(request, product_id):
    product = Products.objects.get(id=product_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        product.name = name
        product.price = price
        product.description = description
        product.image = image

        product.save() 
        messages.success(request, "Product updated successfully!")
        return redirect('home')  

    return render(request, 'updateproduct.html', {'product': product})
    

def delete_product(request, product_id):
    product = Products.objects.get(id=product_id)
    if request.method == 'POST':  
        product.delete()  
        messages.success(request, "Product deleted successfully!")
    return redirect('home')





