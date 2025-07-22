from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_http_methods


def login_view(request):
    """Handle login form submission via HTMX"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Return updated navbar partial - target the entire user section
            html = render_to_string('users/navbar_user_section.html', {
                'user': user
            }, request=request)
            
            # Use HTMX to trigger a page refresh after successful login
            response = HttpResponse(html)
            response['HX-Trigger'] = 'loginSuccess'
            response['HX-Retarget'] = '#user-section'
            response['HX-Reswap'] = 'outerHTML'
            return response
        else:
            # Return just the form content with error message
            html = render_to_string('users/login_form.html', {
                'error': 'Invalid username or password.'
            }, request=request)
            return HttpResponse(html)
    
    return HttpResponse('')


def logout_view(request):
    """Handle logout"""
    logout(request)
    # Return updated navbar partial - user should now be anonymous
    html = render_to_string('users/navbar_user_section.html', {
        'user': request.user  # After logout, this will be AnonymousUser
    }, request=request)
    
    response = HttpResponse(html)
    response['HX-Trigger'] = 'logoutSuccess'
    return response


def register_view(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Set first name if provided
            first_name = request.POST.get('first_name', '').strip()
            if first_name:
                user.first_name = first_name
                user.save()
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            
            # Log the user in automatically
            login(request, user)
            return redirect('index')  # Redirect to main page
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


def login_form_partial(request):
    """Return just the login form partial for HTMX"""
    return render(request, 'users/login_form.html')
