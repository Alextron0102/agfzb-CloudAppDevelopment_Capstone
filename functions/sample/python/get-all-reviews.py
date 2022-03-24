import json
import requests
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from http.client import HTTPConnection
def main(dict):
    databaseName = "reviews"
    try:
        authenticator = IAMAuthenticator(dict['IAM_API_KEY'])
        client = CloudantV1(authenticator=authenticator)
        client.set_service_url(dict['COUCH_URL'])
        if 'dealerId' in dict:
            #Validamos que el dealerId exista en la base de datos
            dealer = client.post_find(
                db="dealerships",
                selector={
                "id": {
                    "$eq": int(dict['dealerId'])}},
                fields=['id','short_name','full_name']
            ).get_result()
            if(len(dealer['docs'])==0):
                raise Exception("Dealer not found")
            else:
                reviews_from_dealer_id = client.post_find(
                    db=databaseName,
                    selector={
                    "dealership": {
                        "$eq": int(dict['dealerId'])}},
                    fields=['id','name','dealership','review','purchase',
                            'purchase_date','car_make','car_model','car_year']
                ).get_result()
                print(reviews_from_dealer_id['docs'])
        else:
            raise Exception("No dealerId provided")
    except ApiException as ce:
        print("unable to connect")
        return {"statusCode": 500, "body": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"statusCode": 500, "body": err}
    except Exception as e:
        print("error", e.args[0])
        return {"statusCode": 400, "body": e.args[0]}
    return {"data": reviews_from_dealer_id['docs']}