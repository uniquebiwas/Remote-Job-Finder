from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from account.managers import CustomUserManager

JOB_TYPE = (
    ('M', "Male"),
    ('F', "Female"),

)

ROLE = (
    ('employer', "Employer"),
    ('employee', "Employee"),
    ('course', "Course"),
)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    role = models.CharField(choices=ROLE,  max_length=10)
    gender = models.CharField(choices=JOB_TYPE, max_length=1)

    phone_number = models.CharField(max_length=10, null=True, blank=True)  # Store phone number as a string
    pdf_document = models.FileField(upload_to='pdf_documents/')

    photo=models.ImageField(upload_to='images',null=True, blank=True, default='images/default_image.png')


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name+ ' ' + self.last_name
    objects = CustomUserManager()
