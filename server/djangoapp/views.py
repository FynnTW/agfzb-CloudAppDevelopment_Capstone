from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from . import restapis
from . import models
from django.views.decorators.csrf import csrf_exempt

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def home_view(request):
        return HttpResponseRedirect(redirect_to="")

# Create an `about` view to render a static about page
# def about(request):
# ...
def about_view(request):
    return render(request, "djangoapp/about.html")

# Create a `contact` view to return a static contact page
#def contact(request):
def contact_view(request):
    return render(request, "djangoapp/contact.html")

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context={}
    if request.method == "GET":
        url = "https://fynnpapadopo-3000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = restapis.get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        context['dealerships'] = dealerships
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealerId):
    context={}
    if request.method == "GET":
        url = f"https://fynnpapadopo-5000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews?id={dealerId}"
        # Get dealers from the URL
        reviews = restapis.get_dealer_reviews_from_cf(url, dealerId)
        # Concat all dealer's short name
        review_texts = '\n'.join([review.review + " " + review.sentiment for review in reviews])
        context['reviews'] = reviews
        context['dealer_id'] = dealerId
        context['carModels'] = models.CarModel.objects.all().filter(dealer_id=dealerId)
        context['carMakes'] = models.CarMake.objects.all().filter()
        # Return a list of dealer short name
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
@csrf_exempt
def add_review(request, dealerId):
    review = {}
    json_payload = {}
    if request.method == "GET":
        context={}
        context['dealer_id'] = dealerId
        context['carModels'] = models.CarModel.objects.all()
        return render(request, 'djangoapp/add_review.html', context)
    url = f"https://fynnpapadopo-5000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
    if request.method == "POST":
        review['name'] = request.user.username
        review['id'] = request.user.username
        review["dealership"] = dealerId
        review["car_model"] = request.POST['car_model']
        review["review"] = request.POST['review'] + " " + review["car_make"]
        review["purchase"] = request.POST['purchase']
        review["purchase_date"] = request.POST['purchase_date']
        review["car_year"] = models.CarModel.objects.get(review["car_model"]).year 
        json_payload["review"] = review
        result = restapis.post_request(url, json_payload, dealerId=dealerId)
        return rediect("djangoapp:index")
