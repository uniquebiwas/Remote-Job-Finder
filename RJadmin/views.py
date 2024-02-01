from .forms import TestimonialForm, CourseForm
from django.contrib.auth.decorators import login_required
from jobapp.models import Testimonial, Course, Enrollment
from .forms import TestimonialForm, CourseForm
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CourseEditForm
from .forms import ChangePasswordForm
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from jobapp.permission import user_is_course

@login_required(login_url=reverse_lazy('RJadmin:login'))
@user_is_course
def admin_page(request):
    # Handling form submissions

    if request.method == 'POST':
        #change password
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully updated...! Please log in with new password.')
            return redirect('account:login')

        # Course form handling
        course_form = CourseForm(request.POST, request.FILES)
        if course_form.is_valid():
            course_form.save()
            messages.success(request, 'Course has been added Sucessfully.')
            return redirect('RJadmin:admin_page')  # Redirect to the same page after form submission
    else:
        
        course_form = CourseForm()
        form = ChangePasswordForm(user=request.user)


    # Fetch all courses
    all_courses = Course.objects.all()

    return render(request, 'RJadmin/admin.html', {
        'course_form': course_form,
        'all_courses': all_courses  # Pass all courses to the template
    })



def enroll_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        room_id = request.POST.get('room_id')

        # Fetch all existing enrollments based on user and course
        enrollments = Enrollment.objects.filter(course_id=course_id)

        for enrollment in enrollments:
            # Update the roomid field for each enrollment
            enrollment.roomid = room_id
            enrollment.save()

            # Schedule the task to delete outdated updates

        messages.success(request, 'Room ID updated successfully.')
        return redirect('RJadmin:admin_page')
    else:
        # Handle other HTTP methods or render a response for GET requests
        return render(request, 'RJadmin/admin.html')



def login_view(request):
    if request.user.is_authenticated:
        # User is already logged in, redirect to the main page
        return redirect('RJadmin:admin_page')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # Check if 'Remember Me' checkbox is selected

        user = authenticate(request, username=username, password=password)

        if user is not None and user.role.lower() == 'course':
            login(request, user)
            if not remember_me:
                # If 'Remember Me' checkbox is not selected, set session expiry to 0 (browser session)
                request.session.set_expiry(0)
            messages.success(request, 'Login successful.')
            return redirect('RJadmin:admin_page')
        else:
            messages.error(request, 'Invalid login credentials or insufficient privileges.')

    return render(request, 'RJadmin/adminlogin.html')



def logout_view(request):
    auth.logout(request)
    # messages.success(request, 'You are Successfully logged out')
    return render(request, 'RJadmin/adminlogin.html')



def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = CourseEditForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successful.')
            return redirect('RJadmin:admin_page')  # Redirect to a page displaying the list of courses
    else:
        form = CourseEditForm(instance=course)
    
    return render(request, 'RJadmin/edit_course.html', {'form': form, 'course': course})



@require_http_methods(["DELETE"])
def delete_course(request, course_id):
    # Get the course to delete
    course = get_object_or_404(Course, id=course_id)

    # Perform the deletion
    course.delete()

    messages.success(request, 'Deleted successfully.')
    return redirect('RJadmin:admin_page') 

@login_required(login_url=reverse_lazy('RJadmin:login'))
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully updated...! Please log in with new password.')
            return redirect('RJadmin:login')
        
    else:
        form = ChangePasswordForm(user=request.user)

    return render(request, 'RJadmin/change_password.html', {'form': form})


