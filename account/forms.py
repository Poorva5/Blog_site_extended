from django import forms
# from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import UserData


##this is a form for creating new user
class RegistrationForm(UserCreationForm):
    
    class Meta:
        model = UserData
        fields = ('name', 'phone', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in (self.fields['name'], self.fields['phone'], self.fields['password1'], self.fields['password2']):
            field.widget.attrs.update({'class': 'form-control' })


#this class is for login user
class LoginForm(forms.ModelForm):
    password = forms.CharField(label= 'Password', widget=forms.PasswordInput)


    class Meta:
        model = UserData
        fields = ('phone', 'password')
        widgets = {
                  'phone':forms.TextInput(attrs={'class':'form-control'}),
                  'password':forms.TextInput(attrs={'class':'form-control'}),
                  
        }

    def __init__(self, *args, **kwargs):
        
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in (self.fields['phone'], self.fields['password']):
            field.widget.attrs.update({'class':'form-control'})

    def clean(self):
        if self.is_valid():

            phone = self.cleaned_data.get('phone')
            password = self.cleaned_data.get('password')
            if not authenticate(phone=phone, password=password):
                raise forms.ValidationError('Invalid Login')