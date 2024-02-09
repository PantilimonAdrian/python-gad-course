"""Views used for account management of the GameTracker App"""
from .forms import RegisterUserForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def register_user_page(request):
    """This view function is used to handle user registration of the app."""
    env = {}

    # Add page information to context
    env["error_message"] = ""
    env["application_name"] = "GameTracker"
    env["marketing_message"] = ("Embark on your gaming journey and start documenting "
                                "your adventures. Join the app today!")

    # Default error message when registration fails
    REGISTRATION_ERROR_MESSAGE = ("A problem occured during the registration process."
                                  "Please make sure your filled your information correctly.")

    if request.method == "POST":
        register_form = RegisterUserForm(request.POST)
        # Check if information provided to the register form is valid
        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data.get("username")
            password = register_form.cleaned_data.get("password1")
            try:
                # Attempt to authenticate and log in the user after succesful registration
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect("home")
            except Exception as error:
                env["error_message"] = REGISTRATION_ERROR_MESSAGE
    else:
        # Add the register form object to the page context.
        register_form = RegisterUserForm()
        env["register_form"] = register_form

    return render(request, "register.html", context=env)


@csrf_protect
def login_user_page(request):
    """This view function is used to handle user login to the app."""
    env = {}

    # Add page information to context
    env["error_message"] = ""
    env["application_name"] = "GameTracker"
    env["marketing_message"] = "Embark on your gaming odyssey! <br> Log into GameTracker now!"
    env["next_url"] = request.GET.get("next", "")

    # Attempt to authenticate/login user if the user sends any data
    # if not then just display the login page that is a part of homepage
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.POST.get("next_url")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            print(next_url)
            if next_url:
                return redirect(next_url)
            else:
                return redirect("home")
        else:
            env["error_message"] = ("An unexpected error occured during the log in process."
                                    " Please ensure your credentials are correct and try again.")

    return render(request, "login.html", context=env)


def logout_user_page(request):
    """This view function is used to handle user logout."""
    logout(request)
    return redirect("home")