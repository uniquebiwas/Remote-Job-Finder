# Import necessary modules and functions from Django
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .forms import ChangePasswordForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.tokens import default_token_generator
from account.models import User  # Import the custom User model
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
# Import necessary forms and custom permissions
from account.forms import *
from jobapp.permission import user_is_employee

# Define a function to handle the success URL after login
def get_success_url(request):
    """
    Determine the success URL after login.

    If 'next' parameter is present in the URL, redirect to that URL.
    Otherwise, redirect to the home page of the job application app.
    """
    if 'next' in request.GET and request.GET['next'] != '':
        return request.GET['next']
    else:
        return reverse('jobapp:home')


# Define a view function for employee registration
def employee_registration(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set the user as inactive until email confirmation
            user.save()

            # Determine the protocol based on the request
            protocol = 'https' if request.is_secure() else 'http'

            # Send email verification
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('account/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'protocol': protocol,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(subject, message, to=[to_email])
            email.content_subtype = "html"
            email.send()

            messages.success(request, 'Please check your email to activate your account.')
            return redirect('account:login')
    else:
        form = EmployeeRegistrationForm()

    context = {
        'form': form
    }

    return render(request, 'account/employee-registration.html', context)

# Define a view function for employer registration
def employer_registration(request):
    """
    Handle the process of employer registration form submission.

    If the request method is POST, validate the form data and create an employer profile.
    Display success message and redirect to the login page.
    If the request method is GET, display an empty employer registration form.
    """
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST, request.FILES)  # Include request.FILES to handle file uploads
        if form.is_valid():
            employer = form.save(commit=False)
            employer.is_active = False
            employer.pdf_document = request.FILES.get('pdf_document')  # Get uploaded PDF file
            employer.save()
            messages.success(request, 'Your profile was successfully created! Please wait for admin authentication.')
            return redirect('account:login')
    else:
        form = EmployerRegistrationForm()

    context = {
        'form': form
    }

    return render(request, 'account/employer-registration.html', context)

# Define a view function for editing employee profile
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def employee_edit_profile(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = EmployeeProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Profile Was Successfully Updated!')
            return redirect(reverse("account:edit-profile", kwargs={'id': user.id}))
    else:
        form = EmployeeProfileEditForm(instance=user)

    context = {
        'form': form
    }

    return render(request, 'account/employee-edit-profile.html', context)

# Define a view function for user login
def user_logIn(request):
    """
    Handle the process of user login.

    If the request method is POST, validate the login form data and authenticate the user.
    If successful, log the user in and redirect to the appropriate success URL or homepage.
    If the request method is GET, display the login form.
    """
    if request.user.is_authenticated:
        # User is already logged in, redirect to the main page
        return render(request, 'jobapp/index.html')
    if request.method == 'POST':
        form = UserLoginForm(request.POST, request=request)  # Pass the request object to the form
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            # Redirect to the appropriate success URL or homepage
            return HttpResponseRedirect(get_success_url(request))
    else:
        form = UserLoginForm(request=request)  # Pass the request object to the form when creating an instance
        
    context = {
        'form': form,
    }

    return render(request, 'account/login.html', context)

# Define a view function for user logout
def user_logOut(request):
    """
    Handle the process of user logout.

    Log the user out and display a success message.
    """
    auth.logout(request)
    messages.success(request, 'You are Successfully logged out')
    return redirect('account:login')


@login_required(login_url=reverse_lazy('account:login'))
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully updated...! Please log in with new password.')
            return redirect('account:login')
        
    else:
        form = ChangePasswordForm(user=request.user)

    return render(request, 'account/change_password.html', {'form': form})


class CustomPasswordResetView(PasswordResetView):
    template_name = 'account/password_reset_form.html'
    email_template_name = 'account/password_reset_email.html'
    success_url = reverse_lazy('account:password_reset_done')
    
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:login')  #  the login URL

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Add a success message
        messages.success(self.request, 'Password reset successful. You can now log in with your new password.')

        return response

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'

def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)  # Use the custom User model
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated. Please login.")
        return redirect('account:login')  # Redirect to the login page
    else:
        messages.error(request, "Invalid Link. Please try again or contact support.")
        return redirect('account:login') 