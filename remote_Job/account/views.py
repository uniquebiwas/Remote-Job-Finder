from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse, reverse_lazy

from account.forms import *
from jobapp.permission import user_is_employee 


def get_success_url(request):

    """
    Handle Success Url After LogIN

    """
    if 'next' in request.GET and request.GET['next'] != '':
        return request.GET['next']
    else:
        return reverse('jobapp:home')





def employee_registration(request):
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


def employer_registration(request):
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



@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_employee
def employee_edit_profile(request, id=id):

    """
    Handle Employee Profile Update Functionality

    """

    user = get_object_or_404(User, id=id)
    form = EmployeeProfileEditForm(request.POST or None, instance=user)
    if form.is_valid():
        form = form.save()
        messages.success(request, 'Your Profile Was Successfully Updated!')
        return redirect(reverse("account:edit-profile", kwargs={
                                    'id': form.id
                                    }))
    context={
        
            'form':form
        }

    return render(request,'account/employee-edit-profile.html',context)



def user_logIn(request):
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



def user_logOut(request):
    """
    Provide the ability to logout
    """
    auth.logout(request)
    messages.success(request, 'You are Successfully logged out')
    return redirect('account:login')


# def user_logIn(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request.POST, request=request)  # Pass the request object to the form
#         if form.is_valid():
#             user = form.get_user()
#             auth.login(request, user)
#             # Redirect to the appropriate success URL or homepage
#             return HttpResponseRedirect(get_success_url(request))
#     else:
#         form = UserLoginForm(request=request)  # Pass the request object to the form when creating an instance

#     context = {
#         'form': form,
#     }

#     return render(request, 'account/login.html', context)
