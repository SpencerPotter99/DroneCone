from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, CustomUserForm
from django.contrib.auth import login
from DroneAdmin.forms import ProfileForm
from django.contrib.auth.decorators import user_passes_test


def RegisterView(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()  # Save the User instance
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user) 
            return redirect('home')
    else:
        user_form = CustomUserCreationForm()
        profile_form = ProfileForm()
        profile_form.drone_owner = False

    return render(request, 'Account/register.html', {'user_form': user_form, 'profile_form': profile_form})


def DroneOwnerRegisterView(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()  # Save the User instance
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user) 
            return redirect('manage_my_drone')
    else:
        initial_data = {'drone_owner': True}

        # Create an instance of the ProfileForm with the initial data
        profile_form = ProfileForm(initial=initial_data)
        user_form = CustomUserCreationForm()

    return render(request, 'DroneCustomer/droneOwnerCreation.html', {'user_form': user_form, 'profile_form': profile_form})


class LoginView(auth_views.LoginView):
    template_name = 'account/login.html'


class LogoutView(auth_views.LogoutView):
    template_name = "account/logout.html"
    http_method_names = ["get", "post", "options"]

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Logout may be done via POST."""
        auth_logout(request)
        messages.success(request, 'Successfully logged out.')
        redirect_to = self.get_success_url()
        if redirect_to != request.get_full_path():
            # Redirect to target page once the session has been cleared.
            return HttpResponseRedirect(redirect_to)
        return super().get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    get = get  # Django4.2 has get = post, but we don't want the user to logout on get request.


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'account/password_change.html'
    success_url = reverse_lazy("account:password_change_done")


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'account/password_change_done.html'


class PasswordResetView(SuccessMessageMixin, auth_views.PasswordResetView):
    template_name = 'account/password_reset.html'
    email_template_name = 'account/password_reset_email.html'
    subject_template_name = 'account/password_reset_subject.txt'
    success_message = ("Please check your email for the password reset instructions. "
                       "You will only receive an email if an account is associated with the provided email.")
    success_url = reverse_lazy('account:password_reset_done')


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_from_key.html'
    success_url = reverse_lazy("account:password_reset_complete")


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_from_key_done.html'


# class ProfileView(LoginRequiredMixin, View):
#     template_name = 'account/user_profile.html'
#     user_form_class = CustomUserForm
#     profile_form_class = ProfileForm

#     def get(self, request, *args, **kwargs):
#         user_form = self.user_form_class(instance=request.user)
#         profile_form = self.profile_form_class(instance=request.user.profile)
#         return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})

#     def post(self, request, *args, **kwargs):
#         user_form = self.user_form_class(request.POST, instance=request.user)
#         profile_form = self.profile_form_class(request.POST, instance=request.user.profile)

#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, 'Your profile is updated successfully')
#             return redirect('account:profile')

#         return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})
