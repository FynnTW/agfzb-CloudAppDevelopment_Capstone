import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    api_key = "S36x4mKcIYgxTkNqvudKgQjrnb-7sxY936XqseHsFgA9"
    json_data = []
    try:
        # Call get method of requests library with URL and parameters
        if api_key is not None:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
    except:
        # If any error occurs
        print("Network exception occurred")
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    json_data = []
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
        json_data = json.loads(response.text)
    except:
        # If any error occurs
        print("Network exception occurred")
    return json_data




def get_dealer_by_id(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            if dealer_doc["id"] != dealerId:
                continue
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = DealerReview(id=dealer_doc["id"], 
                                    name=dealer_doc["name"], 
                                    dealership=dealer_doc["dealership"],
                                   review=dealer_doc["review"], 
                                   purchase=dealer_doc["purchase"],
                                    purchase_date=dealer_doc["purchase_date"],
                                   car_make=dealer_doc["car_make"],
                                   car_model=dealer_doc["car_model"], 
                                   car_year=dealer_doc["car_year"],
                                   sentiment=analyze_review_sentiments(dealer_doc["review"])
                                   )
            results.append(dealer_obj)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    API_KEY = "SKN5Vvf_MjMPT8uCUEpJQCvA_HUJLpANccM2KmTakWSK"
    URL = 'https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/c9ce8039-4e6f-45e4-8f0c-04d87e4581ee'
    authenticator = IAMAuthenticator(API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01', authenticator=authenticator)
    natural_language_understanding.set_service_url(URL)
    try:
        response = natural_language_understanding.analyze(text=dealerreview, features=Features(
            sentiment=SentimentOptions(targets=[dealerreview]))).get_result()
        label = json.dumps(response)
        label = response['sentiment']['document']['label']
        return(label)
    except: # review can be too short for analysis
        return ('')



