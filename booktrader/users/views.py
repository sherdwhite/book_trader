from asgiref.sync import sync_to_async
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

# Create async versions of auth functions
aauthenticate = sync_to_async(authenticate)
alogin = sync_to_async(login)
alogout = sync_to_async(logout)


async def login_view(request):
    """Handle login form submission via HTMX"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = await aauthenticate(request, username=username, password=password)
        if user is not None:
            await alogin(request, user)
            # Return updated navbar partial - target the entire user section
            html = await sync_to_async(render_to_string)(
                "users/navbar_user_section.html", {"user": user}, request=request
            )

            # Use HTMX to trigger a page refresh after successful login
            response = HttpResponse(html)
            response["HX-Trigger"] = "loginSuccess"
            response["HX-Retarget"] = "#user-section"
            response["HX-Reswap"] = "outerHTML"
            return response
        else:
            # Return just the form content with error message
            html = await sync_to_async(render_to_string)(
                "users/login_form.html",
                {"error": "Invalid username or password."},
                request=request,
            )
            return HttpResponse(html)

    return HttpResponse("")


async def logout_view(request):
    """Handle logout"""
    await alogout(request)
    # Return updated navbar partial - user should now be anonymous
    html = await sync_to_async(render_to_string)(
        "users/navbar_user_section.html",
        {"user": request.user},  # After logout, this will be AnonymousUser
        request=request,
    )

    response = HttpResponse(html)
    response["HX-Trigger"] = "logoutSuccess"
    return response


async def register_view(request):
    """Handle user registration"""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if await sync_to_async(form.is_valid)():
            user = await sync_to_async(form.save)()
            # Set first name if provided
            first_name = request.POST.get("first_name", "").strip()
            if first_name:
                user.first_name = first_name
                await sync_to_async(user.save)()

            username = form.cleaned_data.get("username")
            await sync_to_async(messages.success)(
                request, f"Account created for {username}!"
            )

            # Log the user in automatically
            await alogin(request, user)
            return redirect("index")  # Redirect to main page
    else:
        form = UserCreationForm()

    return await sync_to_async(render)(request, "users/register.html", {"form": form})


async def login_form_partial(request):
    """Return just the login form partial for HTMX"""
    return await sync_to_async(render)(request, "users/login_form.html")
