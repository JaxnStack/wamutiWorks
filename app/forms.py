from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import QuestionUpload


# Registration form (using built-in UserCreationForm)
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

# Login form (using built-in AuthenticationForm)
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
# Form for uploading a CSV or Excel file
class QuestionUploadForm(forms.ModelForm):
    class Meta:
        model = QuestionUpload
        fields = ['quiz', 'file']