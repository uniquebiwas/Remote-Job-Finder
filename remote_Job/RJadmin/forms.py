# forms.py
from django import forms
from ckeditor.widgets import CKEditorWidget
from jobapp.models import Testimonial, Course
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.forms import PasswordChangeForm



class TestimonialForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Testimonial
        fields = ['author_name', 'content', 'profile_image']


class CourseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Course
        fields = ['name', 'tag', 'description', 'document', 'image', 'fee', 'shift', 'seat']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'tag': forms.Select(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control-file'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'shift': forms.TextInput(attrs={'class': 'form-control'}),
            'seat': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CourseEditForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())  

    class Meta:
        model = Course
        fields = ['name', 'tag', 'description', 'document', 'image', 'fee', 'shift', 'seat']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'tag': forms.Select(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control-file'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'shift': forms.TextInput(attrs={'class': 'form-control'}),
            'seat': forms.NumberInput(attrs={'class': 'form-control'}),
        }


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

