from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout

from .forms import RegistrationForm

from .models import User

# Create your views here.
def index(request):
    return render(request, "application/index.html")

class Register(View):
    template = 'application/register.html'
    success_url = 'application:index'

    def get(self, request):
        ctx = {
            'form': RegistrationForm(),
        }
        return render(request, self.template, ctx)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            instance = form.save()
            login(request, instance)
            return redirect(self.success_url)
        ctx = {
           'form': form,
        }
        return render(request, self.template, ctx)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("application:index"))

class Login(View):
    template = 'application/login.html'
    success_url = 'application:index'

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse(self.success_url))
        else:
            return render(request, self.template, {
                "error": "Invalid username and/or password."
            })
