from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm

# Import User model from account.models
from account.models import User

# Form for employee registration
class EmployeeRegistrationForm(UserCreationForm):
    MAX_FILE_SIZE_MB = 5  # 5 MB limit for file upload

    # Additional fields for employee registration form
    phone_number = forms.CharField(max_length=10, required=True, label='Phone Number',
                                   widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}))
    pdf_document = forms.FileField(label='Upload your CV (PDF)', required=True,
                                   widget=forms.ClearableFileInput(attrs={'placeholder': 'Upload Your CV'}))
    photo = forms.ImageField(label='Upload a Profile', required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'photo','pdf_document', 'password1', 'password2', 'gender']

    # Customizing form field labels and placeholders
    def __init__(self, *args, **kwargs):
        super(EmployeeRegistrationForm, self).__init__(*args, **kwargs)
        # Set required fields and labels for better user experience
        self.fields['gender'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['pdf_document'].label = "Upload your CV (PDF)"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"
        self.fields['email'].label = "Email"
        self.fields['phone_number'].label = "Phone Number"
        # Set placeholders for input fields
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter Last Name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter Password (at least 8 characters)'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'Enter Phone Number'})
        # self.fields['photo'].widget.attrs.update({'placeholder': 'Enter Photo'})

    # Custom save method to assign role and handle file validation
    def save(self, commit=True):
        user = super(EmployeeRegistrationForm, self).save(commit=False)
        user.role = "employee"  # Assign 'employee' role to the user

        if commit:
            user.save()
        return user

    # Custom validation for PDF document
    def clean_pdf_document(self):
        pdf_document = self.cleaned_data.get('pdf_document')

        if not pdf_document:
            raise forms.ValidationError('Please upload your CV.')

        # Check if the uploaded file is a PDF
        if not pdf_document.name.endswith('.pdf'):
            raise forms.ValidationError('Invalid file format. Please upload a PDF file.')

        # Check file size
        max_size = self.MAX_FILE_SIZE_MB * 1024 * 1024  # Convert MB to bytes
        if pdf_document.size > max_size:
            raise forms.ValidationError('File size must be no more than {} MB.'.format(self.MAX_FILE_SIZE_MB))

        return pdf_document

# Form for employer registration
class EmployerRegistrationForm(UserCreationForm):
    # Additional fields for employer registration form
    pdf_document = forms.FileField(label='Registration Documents (PDF)', required=True,
                                   widget=forms.ClearableFileInput(attrs={'placeholder': 'Upload Your Documents'}))
    phone_number = forms.CharField(max_length=15, required=True, label='Phone Number',
                                   widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'pdf_document', 'password1', 'password2']

    # Customizing form field labels and placeholders
    def __init__(self, *args, **kwargs):
        super(EmployerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].label = "Company Name"
        self.fields['last_name'].label = "Company Address"
        self.fields['pdf_document'].label = "Registration Documents (PDF)"
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'Enter Phone Number'})
        # Set placeholders for input fields
        for field in self.fields.values():
            field.widget.attrs.update({'placeholder': field.label})

    # Custom save method to assign role
    def save(self, commit=True):
        user = UserCreationForm.save(self, commit=False)
        user.role = "employer"  # Assign 'employer' role to the user
        if commit:
            user.save()
        return user

# Form for user login
class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'password-toggle'}),
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(),
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Get request from kwargs
        super(UserLoginForm, self).__init__(*args, **kwargs)

    # Custom clean method for user authentication and session handling
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        remember_me = self.cleaned_data.get("remember_me")

        if email and password:
            self.user = authenticate(email=email, password=password)  # Authenticate user

            try:
                user = User.objects.get(email=email)  # Get user by email
            except User.DoesNotExist:
                raise forms.ValidationError("User Does Not Exist.")

            if not user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")

            if not user.is_active:
               raise forms.ValidationError("Your account is not yet active. Please wait for activation.")
            if user.role.lower() == 'course':
                raise forms.ValidationError("Login not allowed for users with role 'course'.")
        if not remember_me:
            # If "Remember Me" is not checked, set session expiry to 0 (session ends when the browser is closed)
            self.request.session.set_expiry(0)

        return super(UserLoginForm, self).clean(*args, **kwargs)

    # Get authenticated user
    def get_user(self):
        return self.user


# Form for editing employee profile
class EmployeeProfileEditForm(forms.ModelForm):
    photo = forms.ImageField(label='Change Profile Picture',)
    
    pdf_document = forms.FileField(label='Want to change CV (PDF)', required=False,
                                   widget=forms.ClearableFileInput(attrs={'placeholder': 'Upload Your CV'}))
  
    def __init__(self, *args, **kwargs):
        super(EmployeeProfileEditForm, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter Last Name'})
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'Enter Phone Number'})

     
    class Meta:
        model = User
        fields = ['photo',"first_name", "last_name", "phone_number", "gender","pdf_document"]


        # Specify labels for form fields
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone_number': 'Phone Number',
            'gender': 'Gender',
            'photo':'photo'
        }

# Custom form for initiating password reset process
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='Email',  # Label for the email field
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your Email', 'autocomplete': 'email'}),
        # Email input field with placeholder and autocomplete attribute
    )

# Customized password reset form, based on Django's BasePasswordResetForm
class PasswordResetForm(BasePasswordResetForm):
    email = forms.EmailField(
        label='Email',  # Label for the email field
        max_length=254,  # Maximum length for the email field
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your Email', 'autocomplete': 'email'}),
        # Email input field with placeholder and autocomplete attribute
    )


# Change Password code .........
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password: ",
        widget=forms.PasswordInput(attrs={'placeholder': 'Old Password', 'class': 'password-toggle'}),
    )
    new_password1 = forms.CharField(
        label="New Password: ",
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password', 'class': 'password-toggle'}),
    )
    new_password2 = forms.CharField(
        label="Confirm Password: ",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'password-toggle'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')

        if old_password:
            user = self.user

            # Check if the old password is correct
            if not user.check_password(old_password):
                self.add_error('old_password', 'The old password is incorrect.')

        return cleaned_data


class CustomPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text="Enter your new password.",
    )
    
    new_password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The passwords do not match.")

        return cleaned_data
