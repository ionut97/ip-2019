from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class Car(models.Model):
    picture = models.FileField(null=True, upload_to=settings.IMAGES_URL)
    name = models.CharField(max_length=100)
    make = models.CharField(max_length=100, null=True)
    car_model = models.CharField(max_length=100, null=True)
    price = models.IntegerField(null=True)
    fuel = models.CharField(max_length=20, null=True)
    seats = models.IntegerField(null=True)
    power = models.IntegerField(null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mileage = models.IntegerField(null=True)
    year = models.IntegerField(null=True)
    description = models.TextField()

    def __str__(self):
        return self.make + " " + self.name

    @property
    def picture_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url


class SavedAdvertisement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    save_time = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    address = models.TextField()
    approved_by = models.ForeignKey(User, on_delete=None, null=True, related_name='approved_by_user')
    is_bought = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' - ' + self.car.name
