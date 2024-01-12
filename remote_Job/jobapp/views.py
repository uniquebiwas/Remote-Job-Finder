from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse,HttpResponse
from django.core.serializers import serialize
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import json
from django.core.mail import EmailMessage
from account.models import User
from jobapp.forms import *
from jobapp.models import *
from jobapp.permission import *
from .forms import ContactForm
User = get_user_model()


# Home view displaying job listings and pagination
def home_view(request):
    """
    View to display the home page, including job listings and pagination.
    """
    testimonials = Testimonial.objects.all()
    # print(testimonials)
    # Retrieve published jobs ordered by timestamp
    published_jobs = Job.objects.filter(is_published=True).order_by('-timestamp')
    
    # Filter open jobs from the published jobs
    jobs = published_jobs.filter(is_closed=False)
    # print(jobs)
    
    # Count total candidates and total companies
    total_candidates = User.objects.filter(role='employee').count()
    total_companies = User.objects.filter(role='employer').count()
    
    # Create a paginator for the jobs
    paginator = Paginator(jobs, 3)
    page_number = request.GET.get('page', None)
    page_obj = paginator.get_page(page_number)

    if request.is_ajax():
        # AJAX handling
        job_lists = []
        job_objects_list = page_obj.object_list.values()
        for job_list in job_objects_list:
            job_lists.append(job_list)

        # Determine next and previous page numbers for AJAX response
        next_page_number = None
        if page_obj.has_next():
            next_page_number = page_obj.next_page_number()

        prev_page_number = None
        if page_obj.has_previous():
            prev_page_number = page_obj.previous_page_number()

        data = {
            'job_lists': job_lists,
            'current_page_no': page_obj.number,
            'next_page_number': next_page_number,
            'no_of_page': paginator.num_pages,
            'prev_page_number': prev_page_number
        }
        return JsonResponse(data)

    # Prepare context for rendering the template
    context = {
        'total_candidates': total_candidates,
        'total_companies': total_companies,
        'total_jobs': len(jobs),
        'total_completed_jobs': len(published_jobs.filter(is_closed=True)),
        'page_obj': page_obj,
        'testimonials':testimonials
    }
    
    
    # Render the HTML template with the context data
    return render(request, 'jobapp/index.html', context)

# Function to display a list of jobs
def job_list_View(request):
    """
    View to display a list of jobs.
    """

    # Filter and order jobs by timestamp
    job_list = Job.objects.filter(is_published=True, is_closed=False).order_by('-timestamp')
    
    # Create a paginator for the job list
    paginator = Paginator(job_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    
    # Render the HTML template with the context data
    return render(request, 'jobapp/job-list.html', context)

# View for vendors to create a job post
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def create_job_View(request):
    """
    View to provide the ability to create a job post.
    """

    form = JobForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    categories = Category.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            # Save tags
            form.save_m2m()
            messages.success(
                request, 'You have successfully posted your job! Please wait for review.')
            return redirect(reverse("jobapp:single-job", kwargs={'id': instance.id}))

    context = {
        'form': form,
        'categories': categories
    }
    
    # Render the HTML template with the context data
    return render(request, 'jobapp/post-job.html', context)

# View to provide the ability to view job details
def single_job_view(request, id):
    """
    View to provide the ability to view job details.
    """

    job = get_object_or_404(Job, id=id)
    related_job_list = job.tags.similar_objects()

    paginator = Paginator(related_job_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'job': job,
        'page_obj': page_obj,
        'total': len(related_job_list)
    }
    
    # Render the HTML template with the context data
    return render(request, 'jobapp/job-single.html', context)

# View to search for jobs with multiple fields

def search_result_view(request):
    """
    View to search for jobs with multiple fields.
    """

    job_list = Job.objects.order_by('-timestamp')

    # Keywords
    if 'job_title_or_company_name' in request.GET:
        job_title_or_company_name = request.GET['job_title_or_company_name']

        if job_title_or_company_name:
            job_list = job_list.filter(title__icontains=job_title_or_company_name) | job_list.filter(
                company_name__icontains=job_title_or_company_name)

    # Location
    if 'location' in request.GET:
        location = request.GET['location']
        if location:
            job_list = job_list.filter(location__icontains=location)

    # Job Type
    if 'job_type' in request.GET:
        job_type = request.GET['job_type']
        if job_type:
            job_list = job_list.filter(job_type__iexact=job_type)

    paginator = Paginator(job_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Check if there are no results
    no_results = not page_obj.object_list.exists()

    context = {
        'page_obj': page_obj,
        'no_results': no_results,  # Update the flag to check page_obj instead of job_list
    }

    # Render the HTML template with the context data
    return render(request, 'jobapp/result.html', context)

# View to allow users to apply for a job
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def apply_job_view(request, id):
    """
    View to allow users to apply for a job.
    """

    form = JobApplyForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = Applicant.objects.filter(user=user, job=id)
    print(user)
    print("hello")
    if not applicant:
        if request.method == 'POST':
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully applied for this job!')
                return redirect(reverse("jobapp:single-job", kwargs={
                    'id': id
                }))
        else:
            return redirect(reverse("jobapp:single-job", kwargs={
                'id': id
            }))
    else:
        messages.error(request, 'You already applied for the Job!')

        return redirect(reverse("jobapp:single-job", kwargs={
            'id': id
        }))

# View to display user-specific dashboard information
@login_required(login_url=reverse_lazy('account:login'))
def dashboard_view(request):
    """
    View to display
        user-specific dashboard information.
    """

    jobs = []
    savedjobs = []
    appliedjobs = []
    total_applicants = {}
    
    if request.user.role == 'employer':
        # For vendors, fetch their jobs and count applicants for each job
        jobs = Job.objects.filter(user=request.user.id)
        for job in jobs:
            count = Applicant.objects.filter(job=job.id).count()
            total_applicants[job.id] = count

    if request.user.role == 'employee':
        # For employees, fetch saved jobs and applied jobs
        savedjobs = BookmarkJob.objects.filter(user=request.user.id)
        appliedjobs = Applicant.objects.filter(user=request.user.id)
    
    context = {
        'jobs': jobs,
        'savedjobs': savedjobs,
        'appliedjobs': appliedjobs,
        'total_applicants': total_applicants
    }

    return render(request, 'jobapp/dashboard.html', context)

# View to delete a job post
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def delete_job_view(request, id):
    """
    View to delete a job post.
    """

    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:
        job.delete()
        messages.success(request, 'Your Job Post was successfully deleted!')

    return redirect('jobapp:dashboard')

# View to mark a job as complete
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def make_complete_job_view(request, id):
    """
    View to mark a job as complete.
    """
    
    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:
        try:
            job.is_closed = True
            job.save()
            messages.success(request, 'Your Job was marked closed!')
        except:
            messages.success(request, 'Something went wrong !')
            
    return redirect('jobapp:dashboard')

# View to display all applicants for a job
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def all_applicants_view(request, id):
    """
    View to display all applicants for a job.
    """

    all_applicants = Applicant.objects.filter(job=id)

    context = {
        'all_applicants': all_applicants
    }

    return render(request, 'jobapp/all-applicants.html', context)

# View to delete a bookmarked job
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def delete_bookmark_view(request, id):
    """
    View to delete a bookmarked job.
    """

    job = get_object_or_404(BookmarkJob, id=id, user=request.user.id)

    if job:
        job.delete()
        messages.success(request, 'Saved Job was successfully deleted!')

    return redirect('jobapp:dashboard')


# View to display details of an applicant
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def applicant_details_view(request, id):
    """
    View to display details of an applicant.
    """

    applicant = get_object_or_404(User, id=id)
    applicant1 = get_object_or_404(Applicant, user_id=id, job__title=request.GET.get('job_title'))


    context = {
        'applicant': applicant,
        'job_title': applicant1.job.title
    }

    return render(request, 'jobapp/applicant-details.html', context)

# View to bookmark a job
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def job_bookmark_view(request, id):
    """
    View to bookmark a job.
    """

    form = JobBookmarkForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = BookmarkJob.objects.filter(user=request.user.id, job=id)

    if not applicant:
        if request.method == 'POST':
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully saved this job!')
                return redirect(reverse("jobapp:single-job", kwargs={
                    'id': id
                }))
        else:
            return redirect(reverse("jobapp:single-job", kwargs={
                'id': id
            }))
    else:
        messages.error(request, 'You already saved this Job!')

        return redirect(reverse("jobapp:single-job", kwargs={
            'id': id
        }))

# View to handle job updates
@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def job_edit_view(request, id=id):
    """
    View to handle job updates.
    """

    job = get_object_or_404(Job, id=id, user=request.user.id)
    categories = Category.objects.all()
    form = JobEditForm(request.POST or None, instance=job)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # Save tags
        messages.success(request, 'Your Job Post Was Successfully Updated!')
        return redirect(reverse("jobapp:single-job", kwargs={
            'id': instance.id
        }))
    context = {
        'form': form,
        'categories': categories
    }

    return render(request, 'jobapp/job-edit.html', context)

# View to display the about us page
def about_us_view(request):
    return render(request, 'jobapp/about_us.html')

# View to display the terms and conditions page
def terms_condition_view(request):
    return render(request, 'jobapp/terms-condition.html')

# View to handle the contact us form
def contact_us_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            try:
                # Prepare the HTML content of the email
                html_message = render_to_string('jobapp/mail.html', {'name': name})

                send_mail(
                    subject,
                    f'Name: {name}\nEmail: {email}\nMessage: {message}',
                    settings.EMAIL_HOST_USER,
                    ['remotejob007@gmail.com'],  # Replace with the recipient's email address
                    fail_silently=False,
                )

                send_mail(
                    'Message Received, Thanks for Contacting Us' ,
                    message,  # Plain text message, ignored if html_message is present
                    settings.EMAIL_HOST_USER,
                    [email],  # Use the email provided by the user in the form
                    fail_silently=False,
                    html_message=html_message,  # Pass the HTML content here
                )

                messages.success(request, 'Contact form has been successfully sent.')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            messages.error(request, 'Fill out the form completely.')
    else:
        form = ContactForm()  # Create an empty form if the request method is GET
    
    return render(request, 'jobapp/contact_us.html', {'form': form})

# View to send email based on button type (select or reject)
# def send_email(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         email = data.get('email')
#         position = data.get('position')
#         company_name = data.get('company_name')
#         mero_name = data.get('mero_name')
#         button_type = data.get('buttonType')
#         if button_type == 'reject':
#             print('Rejected')
#         elif button_type == 'select':
#             print('Selected')
        
#         # Send email based on button type (select or reject)
#         subject = 'Application Status'
#         template_name = 'jobapp/job_mail.html'
#         context = {
#             'company_name': company_name,
#             'position': position,
#             'mero_name':mero_name,
#             'buttonType': button_type,
#         }

#         try:
#             # Render the email content using the template and context
#             email_content = render_to_string(template_name, context)
#             # Send the email
#             email = EmailMessage(subject, email_content, 'your@example.com', [email])
#             email.content_subtype = "html"
#             email.send()

#             response_data = {'success': True, 'message': 'Email sent successfully!', 'buttonType': button_type}
#         except Exception as e:
#             print(str(e))
#             response_data = {'success': False, 'message': 'Failed to send email.'}
        
#         return JsonResponse(response_data)
#     else:
#         return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def send_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')  # Assuming 'email' is used to uniquely identify the user
        position = data.get('position')
        company_name = data.get('company_name')
        mero_name = data.get('mero_name')
        button_type = data.get('buttonType')

        # Update the status based on the button_type
        if button_type == 'reject':
            status = 'Rejected'
        elif button_type == 'select':
            status = 'Selected'
        else:
            # Handle other cases if needed
            return JsonResponse({'success': False, 'message': 'Invalid button_type'})

        # Find the Applicant based on the User's email
        try:
            user = User.objects.get(email=email)
            job_title=position
            # print(user)
            applicant = Applicant.objects.get(user=user, job__title=job_title)

            # Save the status to the Applicant model
            applicant.status = status
            applicant.save()

            # return JsonResponse({'success': True, 'message': 'Status updated successfully for all applicants.'})

        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found.'})

        # Send email based on button type (select or reject)
        subject = 'Application Status'
        template_name = 'jobapp/job_mail.html'
        context = {
            'company_name': company_name,
            'position': position,
            'mero_name': mero_name,
            'buttonType': button_type,
        }

        try:
            # Render the email content using the template and context
            email_content = render_to_string(template_name, context)
            # Send the email
            email = EmailMessage(subject, email_content, 'your@example.com', [email])
            email.content_subtype = "html"
            email.send()

            response_data = {'success': True, 'message': 'Email sent successfully!', 'buttonType': button_type}
        except Exception as e:
            print(str(e))
            response_data = {'success': False, 'message': 'Failed to send email.'}

        return JsonResponse(response_data)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})



from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Applicant, Job

@require_POST
def reject_all_applicants(request, job_id):
    try:
        # Update the status for all applicants related to the specific job to "Rejected"
        job = Job.objects.get(pk=job_id)
        job.applicant_set.exclude(status="Selected").update(status="Rejected")
        return JsonResponse({'message': 'All applicants for the job rejected successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
