# Import necessary modules and functions from Django
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy

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
    """
    Handle the process of employee registration form submission.

    If the request method is POST, validate the form data and create an employee profile.
    Display success message and redirect to the login page.
    If the request method is GET, display an empty employee registration form.
    """
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST, request.FILES)  # Ensure request.FILES is passed
        if form.is_valid():
            user = form.save(commit=False)
            user.pdf_document = request.FILES.get('pdf_document')  # Use get() to avoid KeyError
            user.save()
            messages.success(request, 'Your Profile Was Successfully Created!')
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
            employer.pdf_document = request.FILES.get('pdf_document')  # Get uploaded PDF file
            employer.save()
            messages.success(request, 'Your Profile Was Successfully Created!')
            return redirect('account:login')
    else:
        form = EmployerRegistrationForm()

    context = {
        'form': form
    }

    return render(request, 'account/employer-registration.html', context)

# Define a view function for editing employee profile
@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_employee
def employee_edit_profile(request, id=id):
    """
    Handle the process of updating employee profile information.

    If the request method is POST, validate the form data and update the employee profile.
    Display success message and redirect to the updated profile page.
    If the request method is GET, display the filled employee profile edit form.
    """
    user = get_object_or_404(User, id=id)
    form = EmployeeProfileEditForm(request.POST or None, instance=user)
    if form.is_valid():
        form = form.save()
        messages.success(request, 'Your Profile Was Successfully Updated!')
        return redirect(reverse("account:edit-profile", kwargs={'id': form.id}))

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

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ChangePasswordForm
from django.contrib import messages

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('account:login')
        
    else:
        form = ChangePasswordForm(user=request.user)

    return render(request, 'account/change_password.html', {'form': form})