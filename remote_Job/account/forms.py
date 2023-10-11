from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
# from phonenumber_field.formfields import PhoneNumberField
# from django_countries.fields import CountryField


from account.models import User

class EmployeeRegistrationForm(UserCreationForm):
    MAX_FILE_SIZE_MB = 5  # 5 MB limit

    phone_number = forms.CharField(max_length=10, required=True, label='Phone Number',
                                   widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}))
    pdf_document = forms.FileField(label='Upload your CV', required=True,
                                   widget=forms.ClearableFileInput(attrs={'placeholder': 'Upload Your CV'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'pdf_document', 'password1', 'password2', 'gender']

    def __init__(self, *args, **kwargs):
        super(EmployeeRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['gender'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].label = "First Name:"
        self.fields['last_name'].label = "Last Name:"
        self.fields['pdf_document'].label = "Upload your CV:"
        self.fields['password1'].label = "Password:"
        self.fields['password2'].label = "Confirm Password:"
        self.fields['email'].label = "Email:"
        self.fields['phone_number'].label = "Phone Number:"

        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Enter First Name',
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Enter Last Name',
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter Email',
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Enter Password',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password',
        })
        self.fields['phone_number'].widget.attrs.update({
            'placeholder': 'Enter Phone Number',
        })

    def save(self, commit=True):
        user = super(EmployeeRegistrationForm, self).save(commit=False)
        user.role = "employee"

        if commit:
            user.save()
        return user

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


class EmployerRegistrationForm(UserCreationForm):
    pdf_document = forms.FileField(label='Registration Documents (PDF)', required=True,
                                   widget=forms.ClearableFileInput(attrs={'placeholder': 'Upload Your Documents'}))
    phone_number = forms.CharField(max_length=15, required=True, label='Phone Number',
                                   widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'pdf_document', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(EmployerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].label = "Company Name"
        self.fields['last_name'].label = "Company Address"
        self.fields['pdf_document'].label = "Registration Documents (PDF)"
        self.fields['phone_number'].widget.attrs.update({
            'placeholder': 'Enter Phone Number',
        })

        for field in self.fields.values():
            field.widget.attrs.update({
                'placeholder': field.label,
            })


    def save(self, commit=True):
        user = UserCreationForm.save(self,commit=False)
        user.role = "employer"
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email =  forms.EmailField(
    widget=forms.EmailInput(attrs={ 'placeholder':'Email',})
) 
    password = forms.CharField(strip=False,widget=forms.PasswordInput(attrs={
        
        'placeholder':'Password',
    }))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("User Does Not Exist.")

            if not user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")

            if not user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user



class EmployeeProfileEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EmployeeProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Name',
            }
        )
        self.fields['phone_number'].widget.attrs.update(
            {
                'placeholder': 'Enter Phone Number',
            }
        )
        # self.fields['pdf_document'].label = "Update Your CV (If you want to: )"

    class Meta:
        model = User
        fields = ["first_name", "last_name", 'phone_number','gender']



