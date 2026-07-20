from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class CustomerRegistrationForm(UserCreationForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):

        model = User

        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):

        user = super().save(commit=False)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:

            user.save()

            UserProfile.objects.create(user=user, role='Customer')

        return user

class CustomerEditForm(forms.ModelForm):

    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:

        model = UserProfile

        fields = [
            'phone_number',
            'address',
            'profile_picture',
        ]

        widgets = {

            'phone_number': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'address': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            ),

            'profile_picture': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            ),

        }

class EmployeeCreationForm(UserCreationForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    profile_picture = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):

        model = User

        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'address',
            'profile_picture',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):

        user = super().save(commit=False)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:

            user.save()

            UserProfile.objects.create(

                user=user,

                role='Employee',

                phone_number=self.cleaned_data['phone_number'],

                address=self.cleaned_data['address'],

                profile_picture=self.cleaned_data['profile_picture'],

            )

        return user
    
class EmployeeEditForm(forms.ModelForm):

    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:

        model = UserProfile

        fields = [
            'phone_number',
            'address',
            'profile_picture',
        ]

        widgets = {

            'phone_number': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'address': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            ),

            'profile_picture': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            ),

        }