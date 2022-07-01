import re
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings

# Create your views here.

@login_required
def account_profile(req: HttpRequest):
    return render(req, "registration/profile.html", { 'user': req.user })

def register_request(request: HttpRequest):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            if "next" in request.POST:
                np = request.POST["next"]
            else:
                np = settings.LOGIN_REDIRECT_URL
            return redirect(np)
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    context = {"register_form": form}

    if "next" in request.GET:
        context["next"] = request.POST["next"]
    else:
        context["next"] = settings.LOGIN_REDIRECT_URL


    return render (request=request, template_name="registration/register.html", context=context)