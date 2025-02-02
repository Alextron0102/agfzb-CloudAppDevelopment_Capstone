import os
from re import A
import requests
import json
from .models import CarMake, CarModel, CarDealer, DealerReview
# import related models here
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
load_dotenv()
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print("GET from {}".format(url))
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=kwargs)
    except:
        print("Error: GET request failed")
    status_code = response.status_code
    print("Status code: {}".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, analyze=False, **kwargs):
    print("POST to {}".format(url))
    try:
        api_key = os.environ.get("WATSON_API_KEY")
        if api_key and analyze==True:
            response = requests.post(url, headers={'Content-Type': 'application/json'},
                                        auth=HTTPBasicAuth('apikey',api_key),
                                        params=kwargs,json=json_payload)
        else:
            response = requests.post(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs,json=json_payload)
    except:
        print("Error: POST request failed")
    status_code = response.status_code
    print("Status code: {}".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["body"]
        for dealer_doc in dealers:
            car_dealer = CarDealer(address=dealer_doc["address"],
                                   city=dealer_doc["city"],
                                   full_name=dealer_doc["full_name"],
                                   dealer_id=dealer_doc["id"],
                                   lat=dealer_doc["lat"],
                                   long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   state=dealer_doc["state"],
                                   st=dealer_doc["st"],
                                   zipcode=dealer_doc["zip"])
            results.append(car_dealer)
    return results

def get_dealers_from_cf_by_id(url, dealer_id, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["body"]
        for dealer_doc in dealers:
            car_dealer = CarDealer(address=dealer_doc["address"],
                                   city=dealer_doc["city"],
                                   full_name=dealer_doc["full_name"],
                                   dealer_id=dealer_doc["id"],
                                   lat=dealer_doc["lat"],
                                   long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   state=dealer_doc["state"],
                                   st=dealer_doc["st"],
                                   zipcode=dealer_doc["zip"])
            if car_dealer.dealer_id == dealer_id:
                results.append(car_dealer)
    
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url, dealerId=dealer_id)
    #print(json_result)
    if json_result:
        reviews = json_result["body"]
        for review_doc in reviews:
            dealer_review = DealerReview(
                review_id=review_doc["id"],
                dealership=review_doc["dealership"],
                name=review_doc["name"],
                purchase=review_doc["purchase"],
                review=review_doc["review"],
                purchase_date=review_doc["purchase_date"] if review_doc["purchase"] else None,
                car_make=review_doc["car_make"] if review_doc["purchase"] else None,
                car_model=review_doc["car_model"] if review_doc["purchase"] else None,
                car_year=review_doc["car_year"] if review_doc["purchase"] else None,
                sentiment=None)
            if api_key:
                dealer_review.sentiment = analyze_review_sentiments(dealer_review.review)
            results.append(dealer_review)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/8802e40a-4cc1-4351-9ea6-e5a9644bb4f8/v1/analyze?version=2021-08-01"
    params = {
        "text": dealerreview,
        "features": {
            "sentiment": {}
        }
    }
    json_result = post_request(url,analyze=True,json_payload=params)
    print(json_result)
    if json_result:
        sentiment = json_result["sentiment"]["document"]["label"]
    return sentiment


