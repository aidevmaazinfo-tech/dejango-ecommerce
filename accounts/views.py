from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomerRegistrationForm, CustomerProfileForm
from .models import User
from orders.models import Order  # <-- Import your Order model

def register_view(request):
    if request.user.is_authenticated:
        return redirect('products:product_list')
        
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.Roles.CUSTOMER
            user.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('products:product_list')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile')
    else:
        form = CustomerProfileForm(instance=request.user)
    
    # Retrieves orders related to request.user
    orders = request.user.orders.all()
    
    return render(request, 'accounts/profile.html', {
        'form': form,
        'orders': orders
    })