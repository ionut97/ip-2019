from django.urls import path

from . import views

app_name = 'web_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('cars/', views.cars_page, name='cars'),
    path('car_dy/', views.cars, name='car_dy'),
    path('car_s/', views.car_search, name='search'),
    path('car/<int:cid>', views.car_details, name='details'),
    path('save_advertisement/<int:cid>', views.save_advertisement, name='save_advertisement'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('compare/', views.compare, name='compare'),
]
