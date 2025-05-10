from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Job, Application, Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    address = forms.CharField(required=True)
    contact = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'address', 'contact', 'password1', 'password2']


class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'company_name',
            'job_title',
            'location',
            'employment_type',
            'experience_level',
            'salary',
            'description',
        ]


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['message', 'resume']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'address', 'contact_number']


class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']


class EditSkillsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['skills']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }
