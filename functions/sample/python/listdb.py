import json
import requests
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
def main(dict):
    databaseName = "dealerships"
    try:
        authenticator = IAMAuthenticator(dict['IAM_API_KEY'])
        client = CloudantV1(authenticator=authenticator)
        client.set_service_url(dict['COUCH_URL'])
        print("Databases: {0}".format(client.get_all_dbs().get_result()))
    except ApiException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}
    return {"dbs": client.get_all_dbs().get_result()}