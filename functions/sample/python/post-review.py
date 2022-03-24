import json
import requests
from ibmcloudant.cloudant_v1 import Document, CloudantV1
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
def main(dict):
    databaseName = "reviews"
    try:
        authenticator = IAMAuthenticator(dict['IAM_API_KEY'])
        client = CloudantV1(authenticator=authenticator)
        client.set_service_url(dict['COUCH_URL'])
        #Validamos que el dealerId exista en la base de datos
        dealer = client.post_find(
            db="dealerships",
            selector={
            "id": {
                "$eq": int(dict['review']['dealership'])}},
            fields=['id','short_name','full_name']
        ).get_result()
        if(len(dealer['docs'])==0):
            raise Exception("Dealer not found")
        else:
            response = client.post_document(db=databaseName,
                                             document=dict['review']
                                             ).get_result()
            print(response)
    except ApiException as ce:
        print("unable to connect")
        return {"statusCode": 500, "body": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"statusCode": 500, "body": err}
    return {"statusCode": 200, "body": "posted correctly"}
