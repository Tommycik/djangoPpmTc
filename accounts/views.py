from uuid import uuid4

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from recipes.models import Recipe
from recipes.views import RecentPageView
from .forms import UserRegisterForm, ForgotForm
from .functions import ForgotEmail, sendEmail
from .models import Cook
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import DetailView


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            htmly = get_template('registration/signupSuccess.html')
            d = {'username': username}
            subject, from_email, to = 'Welcome', 'tcRicette@outlook.it', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, "registration/signup.html", {'form': form, 'title': 'Register Here'})


def Login(request):
    msg = ""
    if request.method == 'GET':
        request.session['previous_page'] = request.META.get('HTTP_REFERER', "/")
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            if not request.session.__contains__("previous_page"):
                return redirect("/")
            control = request.session['previous_page']
            check = [request.build_absolute_uri(reverse_lazy("signup")),
                     request.build_absolute_uri(reverse_lazy("login")),
                     request.build_absolute_uri(reverse_lazy("password_reset_complete")),
                     request.build_absolute_uri(reverse_lazy("password_reset")),
                     request.build_absolute_uri(reverse_lazy("password_reset_done"))
                     ]
            if control in check:
                return redirect("/")
            else:
                return redirect(control)
        else:
            messages.info(request, f'account done not exit plz sign in')
            msg = "Username or password are incorrect"
    form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form, 'title': 'Log In', 'msg': msg})


class DetailAccountView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "../templates/detailAccount.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Your Account Information"
        return context


@login_required()
def delete_user(request):
    context = {}

    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == 'POST':
        user = request.user
        d = {'username': user.username}
        email = user.email
        user.delete()
        htmly = get_template('registration/deleteSuccess.html')
        subject, from_email, to = 'Goodbye', 'tcRicette@outlook.it', email
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return redirect("home")
    else:
        context['object'] = 'Your account'
        context['title'] = "Delete Account"
    return render(request, '../templates/delete.html', context=context)


class FavouritesPageView(RecentPageView):

    def get_queryset(self):
        queryset = Cook.objects.get(title=self.request.user).favourites.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Your Favourite Recipes "
        return context


@login_required
def favourite_add(request, pk):
    cook = Cook.objects.get(title=request.user)
    obj = get_object_or_404(Recipe, pk=pk)
    fav_num = obj.favourites
    favourites = cook.favourites.all()
    if favourites.filter(pk=pk).exists():
        fav_num -= 1
        cook.favourites.remove(pk)
    else:
        cook.favourites.add(pk)
        fav_num += 1
    obj.favourites = fav_num
    obj.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', "/"))
