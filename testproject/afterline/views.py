from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def account_profile(req: HttpRequest):
    return render(req, "registration/profile.html", { 'user': req.user })