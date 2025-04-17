from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Contact, Category
from .forms import ContactForm
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


def index(request):
    featured_cars = Car.objects.filter(is_featured=True)[:3]
    formula1_cars = Car.objects.filter(category__name="Formula 1")[:3]
    return render(request, 'index.html', {
        'featured_cars': featured_cars,
        'formula1_cars': formula1_cars
    })

def car_list(request):
    cars = Car.objects.all()
    categories = Category.objects.all()
    search = request.GET.get('search')
    category = request.GET.get('category')
    sort = request.GET.get('sort')
    
    if search:
        cars = cars.filter(make__icontains=search) | cars.filter(model__icontains=search)
    if category:
        cars = cars.filter(category__name=category)
    if sort == 'price_asc':
        cars = cars.order_by('price')
    elif sort == 'price_desc':
        cars = cars.order_by('-price')
    
    paginator = Paginator(cars, 10)  # 10 cars per page
    page = request.GET.get('page')
    cars = paginator.get_page(page)
    
    return render(request, 'car_list.html', {
        'cars': cars,
        'categories': categories,
        'search': search,
        'sort': sort
    })

def car_detail(request, id):
    car = get_object_or_404(Car, id=id)
    related_cars = Car.objects.filter(category=car.category).exclude(id=car.id)[:3]
    return render(request, 'car_detail.html', {'car': car, 'related_cars': related_cars})

from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ContactForm
from .models import Car

def contact(request):
    car_id = request.GET.get('car_id')
    car = None
    if car_id:
        car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            if car:
                contact.car = car
            contact.save()
            if car:
                return redirect(f"{reverse('contact_success')}?car_id={car.id}")
            else:
                return redirect('contact_success')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form, 'car': car})

def contact_success(request):
    car_id = request.GET.get('car_id')
    car = None
    if car_id:
        car = get_object_or_404(Car, id=car_id)
    return render(request, 'contact_success.html', {'car': car})
