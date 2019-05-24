from django import forms
from django.contrib.auth.models import User

from .models import Car

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class NewAdvertisement(forms.ModelForm):

    make = forms.ChoiceField(required=True)
    make._set_choices(value=(
        ("Audi", "Audi"),
        ("BMW", "BMW"),
        ("Volkswagen", "Volkswagen")
    ))

    price = forms.IntegerField(required=False)
    fuel = forms.ChoiceField(required=True)
    fuel._set_choices(value=(
        ("Petrol", "Petrol"),
        ("Diesel", "Diesel"),
        ("Electric", "Electric"),
        ("Hybrid", "Hybrid")
    ))
    seats = forms.IntegerField(required=False)
    power = forms.IntegerField(required=False)

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
