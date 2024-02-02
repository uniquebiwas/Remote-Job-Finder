from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model()


from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager




JOB_TYPE = (
    ('1', "Full time"),
    ('2', "Part time"),
    ('3', "Internship"),
)

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Job(models.Model):

    user = models.ForeignKey(User, related_name='User', on_delete=models.CASCADE) 
    title = models.CharField(max_length=300)
    description = RichTextField()
    tags = TaggableManager()
    location = models.CharField(max_length=300)
    job_type = models.CharField(choices=JOB_TYPE, max_length=1)
    category = models.ForeignKey(Category,related_name='Category', on_delete=models.CASCADE)
    salary = models.CharField(max_length=30, blank=True)
    company_name = models.CharField(max_length=300)
    company_description = RichTextField(blank=True, null=True)
    url = models.URLField(max_length=200)
    last_date = models.DateField()
    is_published = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

 

class Applicant(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)
    status = models.CharField(max_length=10, blank=True, null=True,default="Pending")

    def __str__(self):
        return self.job.title

class BookmarkJob(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.job.title



class Testimonial(models.Model):
    author_name = models.CharField(max_length=255)
    content = models.TextField()
    profile_image = models.ImageField(upload_to='testimonial_images/', null=True, blank=True)

    def __str__(self):
        return self.author_name

class Course(models.Model):
    COURSE_TAGS = [
        ('paid', 'Paid'),
        ('free', 'Free'),
            ]

    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=10, choices=COURSE_TAGS, default='paid')
    description = RichTextField()
    document = models.FileField(upload_to='course_pdfs/', null=True, blank=True)
    image = models.ImageField(upload_to='course_images',null=True,blank=True)
    fee = models.CharField(max_length=255,null=True,blank=True)
    shift = models.CharField(max_length=255,null=True,blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    seat = models.IntegerField(null=True,blank=True)


    def __str__(self):
        return self.name




class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)
    roomid = models.CharField(max_length=10, blank=True, null=True, default='')

    def __str__(self):
        return self.course.name
