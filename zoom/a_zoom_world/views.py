from django.shortcuts import render
from django.template import RequestContext
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from PIL import Image


# Create your views here.


#-----New User----#
def new_user(request):
    context = RequestContext(request)
    username = None
    email = None
    password = None
    user_success = None
    user_created = None
    if request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print("username ", username)

        user = authenticate(username=username, password=password, email=email)
        if user is not None:
            if user.is_active:
                user_created = True
            else:
                user_created = False
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            user.is_active = True
            user_success = True
            return HttpResponseRedirect('/zoom/zoom_user_profile')

    return render(request, 'new_user.html', {'success': user_success, 'created': user_created, 'username': username}, context)
    # registered = False
    # if request.method == 'POST':
    #     user_form = Login(data=request.POST)
    #
    #     if user_form.is_valid():
    #         user = user_form.save()
    #         user.set_password(user.password)
    #         user.save()
    #
    #         registered = True
    #
    #         return HttpResponseRedirect("/zoom/homepage_properties")
    #     else:
    #         print(user_form.errors)
    # else:
    #     user_form = Login()
    #
    # return render(request, 'new_user.html', {'user_form': user_form, 'registered': registered})


     #----This is for a user already in the system ----#

def login_user(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = authenticate(username=username, password=password, email=email)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/zoom/homepage_properties')

            else:
                return HttpResponse("It seems this account is not valid.")
        else:
            print("Login Information is Invalid")
            return HttpResponse("Login Information is Invalid")

    else:
        return render(request, 'log_in.html')

#---logout---#


def log_out(request):
    logout(request)

    return HttpResponseRedirect("/")

#----------zoom_user_profile -------------#


def zoom_user(request):
    user_profile = ZoomUser.objects.all()

    return render(request, 'zoom_user_profile.html', user_profile)


@cache_page(60 * 15)  # Cache for 15 minutes
@vary_on_cookie
@login_required(login_url='/')
def properties_listing(request):
    # Optimized query to prevent N+1 queries
    # Use select_related for foreign keys and prefetch_related for many-to-many
    listings = Property.objects.select_related(
        'type_id', 'address'
    ).prefetch_related(
        'photo_property'
    ).all()
    
    # Pre-fetch featured photos to avoid additional queries in template
    for property_item in listings:
        try:
            property_item.picture = property_item.photo_property.filter(featured=True).first()
        except:
            property_item.picture = None

    return render(request, 'homepage_properties.html', {'listing': listings})


@cache_page(60 * 30)  # Cache for 30 minutes
@login_required(login_url='/')
def property_description(request, property_id):
    # Optimized query with select_related
    property_info = Property.objects.select_related(
        'type_id', 'address'
    ).prefetch_related(
        'photo_property', 'property_amenity', 'property_allergens', 
        'property_vehicle', 'property_access'
    ).get(pk=property_id)
    
    try:
        feature_photo = property_info.photo_property.filter(featured=True).first()
    except:
        feature_photo = None

    return render(request, 'big_description.html', {'property': property_info, 'feature_photo': feature_photo})


@login_required(login_url='/')
def new_listing(request):


    return render(request, 'new_listing.html')


@cache_page(60 * 30)  # Cache for 30 minutes
@login_required(login_url='/')
def property_gallery_page(request, property_id):
    # Optimized query to get photos directly
    photo_gallery = Photo.objects.filter(
        property_photos__pk=property_id
    ).select_related().all()
    
    return render(request, 'property_gallery.html', {'photo_gallery': photo_gallery, 'property_id': property_id})


@cache_page(60 * 60)  # Cache for 1 hour
def about_us(request):
    return render(request, 'about_us.html')

@cache_page(60 * 60)  # Cache for 1 hour
def contact_us(request):
    return render(request, 'contact_us.html')

@cache_page(60 * 60)  # Cache for 1 hour
def privacy_policy(request):
    return render(request, 'privacy_policy.html')

@cache_page(60 * 60)  # Cache for 1 hour
def terms_of_use(request):
    return render(request, 'terms_of_use.html')

#----------------------- Update Classes


class UserUpdateMain(UpdateView):
    model = User
    fields = '__all__'
