from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm

class RegisterView(View):
    template_name = 'registration/register.html'

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # optionally immediately log the user in
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('blog:post_list')
        return render(request, self.template_name, {'form': form})


from django.contrib.auth.decorators import login_required
@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('blog:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'blog/profile.html', context)

# Create your views here.

from django.http import HttpResponse

def login_view(request):
    return HttpResponse("Login page")

def register_view(request):
    return HttpResponse("Register page")

def profile_view(request):
    return HttpResponse("Profile page")
