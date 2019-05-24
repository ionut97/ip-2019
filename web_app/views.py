from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import UserForm, CompareForm, NewAdvertisement
from .models import Car, SavedAdvertisement
import operator
from functools import reduce
import pickle

MODEL = None
DATASET = None
MATRIX = None


def getMakes():
    makes = []

    for index, row in DATASET.iterrows():
        if row['Make'] not in makes:
            makes.append(row['Make'])

    return makes


def getModels(make):
    models = []

    for index, row in DATASET.iterrows():
        if (row['Make'] == make and row['Model'] not in models):
            models.append(row['Model'])

    return models


def estimatePrice(make, carmodel, year, mileage):
    index_X = 0

    for index, row in DATASET.iterrows():
        if (row['Make'] == make and row['Model'] == carmodel):
            index_X = index

    variable = MATRIX[index_X]
    variable[-1] = mileage
    variable[-2] = year
    variable2 = []
    variable2.append(variable)
    variable2.append(variable)
    return int(MODEL.predict(variable2)[0])


def init_model():
    print("Loading model")
    global MODEL
    global DATASET
    global MATRIX

    MODEL = pickle.load(open("ML/model.pkl", "rb"))
    DATASET = pickle.load(open("ML/dataset.pkl", "rb"))
    MATRIX = pickle.load(open("ML/matrix.pkl", "rb"))

    print("estimare: ", estimatePrice("Audi", "A3", 2010, 2500))

init_model()


def index(request):
    return render(request, 'web_app/index.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('web_app:cars')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('web_app:cars')
            else:
                return render(request, 'web_app/login.html', {'error_message': 'Your account has not been activated!'})
        else:
            return render(request, 'web_app/login.html', {'error_message': 'Invalid login'})
    return render(request, 'web_app/login.html')


def logout_user(request):
    logout(request)
    return redirect('web_app:index')


def register(request):
    if request.user.is_authenticated:
        return redirect('web_app:cars')
    uform = UserForm(request.POST or None)
    if uform.is_valid():
        user = uform.save(commit=False)
        username = uform.cleaned_data['username']
        password = uform.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('web_app:dashboard')

    context = {
        "uform": uform,
    }

    return render(request, 'web_app/register.html', context)


def cars_page(request, pg=1):

    # Each page has 9 requests. That is fixed.
    start = (pg-1) * 9
    end = start + 9

    car_list = Car.objects.all()[start:end]
    context = {
        'cars': car_list
    }

    return render(request, 'web_app/cars.html', context)


def car_search(request):
    if request.method == 'GET':
        if request.GET.get('search'):
            search = request.GET.get('search')
        else:
            search = ''
        if request.GET.get('start'):
            start = int(request.GET.get('start'))
        else:
            start = 0
        if request.GET.get('end'):
            end = int(request.GET.get('end'))
        else:
            end = 9

        objs = Car.objects.filter(
            Q(make__icontains=search) |
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(car_model__icontains=search)
        )[start:end]
        data = serializers.serialize('json', objs)
        return HttpResponse(data)


def cars(request):
    if request.method == 'GET':
        if request.GET.get('start'):
            start = int(request.GET.get('start'))
        else:
            start = 0
        if request.GET.get('end'):
            end = int(request.GET.get('end'))
        else:
            end = 9
        if request.GET.get('make'):
            make = request.GET.get('make')
            if make == 'all':
                make = ''
        else:
            make = ''
        if request.GET.get('cost_min'):
            cost_min = int(float(request.GET.get('cost_min')))
        else:
            cost_min = 0
        if request.GET.get('cost_max'):
            cost_max = int(float(request.GET.get('cost_max')))
        else:
            cost_max = 999999999
        if request.GET.get('fuel'):
            fuel = request.GET.getlist('fuel')
        else:
            fuel = ['petrol', 'diesel', 'electric', 'hybrid']

        objs = Car.objects.filter( 
            Q(make__icontains=make) &
            Q(price__gte=cost_min) &
            Q(price__lte=cost_max) &
            (reduce(operator.or_, (Q(fuel__icontains=x) for x in fuel)))
        )[start:end]
    else:
        objs = Car.objects.all()[:9]

    data = serializers.serialize('json', objs)
    return HttpResponse(data)


def car_details(request, cid):
    car = Car.objects.get(pk=cid)
    context = {
        'car': car
    }

    print(car.picture.url)
    return render(request, 'web_app/car_details.html', context)


def save_advertisement(request, cid):
    if not request.user.is_authenticated:
        return redirect('web_app:login')
    user = request.user
    car = Car.objects.get(pk=cid)

    if request.method == 'POST':
        try:
            new = SavedAdvertisement(
                user=user,
                car=car,
                amount=car.price,
            ).save()

            return HttpResponse("The ad has been saved!")
        except Exception as e:
            return HttpResponse("Uh Oh! Something's wrong! Report to the developer with the following error" +
                                e.__str__())
    return HttpResponseForbidden()


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('web_app:login')

    user = request.user
    new_ad = NewAdvertisement(request.POST or None, request.FILES or None)
    if new_ad.is_valid():
        car = new_ad.save(commit=False)
        car.added_by = user
        car.save()

        if not car.price:
            car.price = estimatePrice(car.make, car.car_model, car.year, car.mileage)

        car.picture.name = car.picture.name.strip('web_app')
        car.save()
        return redirect('web_app:cars')

    saved_ads = SavedAdvertisement.objects.filter(user=user)
    my_cars = Car.objects.filter(added_by=user)

    context = {
        'saved_ads': saved_ads,
        'new_ad': new_ad,
        'my_cars': my_cars
    }

    return render(request, 'web_app/dashboard.html', context)


def compare(request):

    form = CompareForm(request.POST or None)
    if request.method == 'POST':
        car1 = int(request.POST['car1'])
        car2 = int(request.POST['car2'])

        car1 = Car.objects.get(pk=car1)
        car2 = Car.objects.get(pk=car2)

        data = {
            'car1_id': car1.id,
            'car1_name': car1.brand + " " + car1.name,
            'car1_pic': car1.picture.url,
            'car1_price': car1.price,
            'car1_seats': car1.seats,
            'car1_tank_capacity': car1.tank_capacity,
            'car1_transmission': car1.transmission,
            'car1_gears': car1.gears,
            'car1_engine_displacement': car1.engine_displacement,
            'car1_power': car1.power,
            'car1_dimensions': car1.dimensions,
            'car2_id': car2.id,
            'car2_name': car2.brand + " " + car2.name,
            'car2_pic': car2.picture.url,
            'car2_price': car2.price,
            'car2_seats': car2.seats,
            'car2_tank_capacity': car2.tank_capacity,
            'car2_transmission': car2.transmission,
            'car2_gears': car2.gears,
            'car2_engine_displacement': car2.engine_displacement,
            'car2_power': car2.power,
            'car2_dimensions': car2.dimensions,
        }

        html = '''
        <table class="table table-bordered" id="cmpTable">
            <tbody>
            <tr>
                <td>
                </td>
                <td>
                    <a href="car/{car1_id}">{car1_name}</a>
                </td>
                <td>
                    <a href="car/{car2_id}">{car2_name}</a>
                </td>
            </tr>
            <tr>
                <td>
                </td>
                <td>
                    <img class="img-fluid" src="{car1_pic}" alt="">
                </td>
                <td>
                    <img class="img-fluid" src="{car2_pic}" alt="">
                </td>
            </tr>
            <tr>
                <td>
                    Price (in &euro;)
                </td>
                <td>
                    {car1_price}
                </td>
                <td>
                    {car2_price}
                </td>
            </tr>
            <tr>
                <td>
                    Seating capacity
                </td>
                <td>
                    {car1_seats}
                </td>
                <td>
                    {car2_seats}
                </td>
            </tr>
            <tr>
                <td>
                    Fuel Tank Capacity (litres)
                </td>
                <td>
                    {car1_tank_capacity}
                </td>
                <td>
                    {car2_tank_capacity}
                </td>
            </tr>
            <tr>
                <td>
                    Transmission type
                </td>
                <td>
                    {car1_transmission}
                </td>
                <td>
                    {car2_transmission}
                </td>
            </tr>
            <tr>
                <td>
                    Gears
                </td>
                <td>
                    {car1_gears}
                </td>
                <td>
                    {car2_gears}
                </td>
            </tr>
            <tr>
                <td>
                    Engine displacement (cc)
                </td>
                <td>
                    {car1_engine_displacement}
                </td>
                <td>
                    {car2_engine_displacement}
                </td>
            </tr>
            <tr>
                <td>
                    Maximum power (PS)
                </td>
                <td>
                    {car1_power}
                </td>
                <td>
                    {car2_power}
                </td>
            </tr>
            <tr>
                <td>
                    Dimensions (mm)
                </td>
                <td>
                    {car1_dimensions}
                </td>
                <td>
                    {car2_dimensions}
                </td>
            </tr>
            </tbody>
        </table>
        '''.format(**data)

        return HttpResponse(html)

    context = {
        'form': form
    }

    return render(request, 'web_app/compare.html', context)
