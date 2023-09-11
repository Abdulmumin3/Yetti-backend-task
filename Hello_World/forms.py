# from django import forms
# # from django.forms import ModelForm
# from .models import User
# from django.contrib.auth.forms import UserCreationForm

# from django.forms import ModelForm
# from .models import User

# class CustomUserCreateForm(ModelForm):
#     email = forms.EmailField()
#     password = forms.CharField(max_length=128, widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ( 'email', 'password')


# # class (UserCreationForm):
# # 	class Meta:
# # 		model = User
# # 		fields = ['username', 'email', 'password1', 'password2']

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # Import your custom user model

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')  # Include other fields as needed
