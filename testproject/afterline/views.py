from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404

from . import models
from .forms import CreateCampaignForm, NewUserForm


# Create your views here.

@login_required
def account_profile(req: HttpRequest):
    return render(req, "registration/profile.html", {'user': req.user})


def register_request(request: HttpRequest):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")

            if "next" in request.GET:
                np = request.GET["next"]
            else:
                np = settings.LOGIN_REDIRECT_URL
            return redirect(np)
        messages.error(request, "Unsuccessful registration. Invalid information.")
        if "next" in request.POST:
            np = request.POST["next"]
        else:
            np = settings.LOGIN_REDIRECT_URL
        context = {"register_form": form, "next": np}

        return render(request=request, template_name="registration/register.html", context=context)

    form = NewUserForm()
    context = {"register_form": form}

    if "next" in request.GET:
        context["next"] = request.GET["next"]
    else:
        context["next"] = settings.LOGIN_REDIRECT_URL

    return render(request=request, template_name="registration/register.html", context=context)


@login_required
def create_campaign(request: HttpRequest):
    if request.method == "POST":
        form = CreateCampaignForm(request.user, request.POST)
        if form.is_valid():
            campaign = form.save()
            return redirect(f"/campaign/{campaign.id}/")

        return render(request=request, template_name="afterline/campaign/create.html", context={"form": form})

    form = CreateCampaignForm(request.user)
    return render(request=request, template_name="afterline/campaign/create.html", context={"form": form})

@login_required
def view_campaign(request: HttpRequest, id: int):
    camp = get_object_or_404(models.Campaign, pk=id)
    return render(request=request, template_name="afterline/campaign/view.html", context={"campaign": camp})

@login_required
def my_campaigns(request: HttpRequest):
    user = models.AfterlineUser.objects.get(user=request.user)
    ran_games = models.Campaign.objects.filter(game_master=user)
    players = models.Player.objects.filter(user=user)
    member_games = []
    for plr in players:
        member_games.append(plr.game)

    return render(request=request, template_name="afterline/campaign/list.html", context={"ran_games": ran_games,
                                                                                          "member_games": member_games})
