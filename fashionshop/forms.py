from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from fashionshop.models import Profile, Review, Address

MAX_UPLOAD_SIZE = 2500000

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label='Username')
    password = forms.CharField(max_length=200,
                               label='Password',
                               widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid Email/Password")
        return cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, label='Username')
    password = forms.CharField(max_length=200,
                               label='Password',
                               widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=200,
                                       label='Confirm',
                                       widget=forms.PasswordInput())
    email = forms.CharField(max_length=50,
                            label='E-mail',
                            widget=forms.EmailInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['nickname','review_title','review','rating','review_picture']
        widgets = {
           'nickname': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder':"Example: Sammy111"
                }),
            'review_title': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder':"Title your review"
                }),
            'review_picture':forms.FileInput(attrs={}),
            'review': forms.Textarea(attrs={
                'class': "form-control",
                'placeholder':"Tell us what you think"
                })
            
        }
        labels = {
                    'nickname':'Nickname',
                    'review_title':'Title',
                    'review':'Review',
                    'review_picture': 'Product Pic',
                    'rating':'Rating'
                }


class AddressForm(forms.Form):
    fname=forms.CharField(max_length=50)
    lname=forms.CharField(max_length=50)
    country = forms.ChoiceField()
    street_address=forms.CharField(max_length=255)
    email=forms.EmailField()
    city= forms.CharField(max_length=20)
    state = forms.CharField(max_length=20)
    phone_number=forms.IntegerField()
    postcode = forms.IntegerField()
