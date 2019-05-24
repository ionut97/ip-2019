from django import forms
from django.contrib.auth.models import User

from .models import Car
from django.conf import settings


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class NewAdvertisement(forms.ModelForm):

    make = forms.CharField(required=True)
    car_model = forms.CharField(required=True)
    year = forms.IntegerField(required=True)
    mileage = forms.IntegerField(required=True)
    #help
    #picture = forms.FileField(required=False, upload_to=settings.IMAGES_URL)
    name = forms.CharField(max_length=100)
    price = forms.IntegerField(required=False)
    fuel = forms.CharField(max_length=20, required=False)
    seats = forms.IntegerField(required=False)
    power = forms.IntegerField(required=False)
    description = forms.Textarea()

    class Meta:
        model = Car

        fields = '__all__'
        exclude = ('added_by',)


class CompareForm(forms.Form):

    car1 = forms.ModelChoiceField(
        Car.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={'class': 'selectpicker', 'data-live-search': "true"}
        )
    )
    car2 = forms.ModelChoiceField(
        Car.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={'class': 'selectpicker', 'data-live-search': "true"}
        )
    )
