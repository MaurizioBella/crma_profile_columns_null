import os
from simple_salesforce import Salesforce
from simple_salesforce.exceptions import SalesforceAuthenticationFailed
from dotenv import load_dotenv
load_dotenv()

SFDC_SANDBOX = os.getenv("SFDC_SANDBOX")
SFDC_INSTANCE_URL = os.getenv("SFDC_INSTANCE_URL")
SFDC_USERNAME = os.getenv("SFDC_USERNAME")
SFDC_PASSWORD = os.getenv("SFDC_PASSWORD")
SFDC_SECURITY_TOKEN = os.getenv("SFDC_SECURITY_TOKEN")


def login():
    sf = None
    print('SFDC_INSTANCE_URL %s', SFDC_INSTANCE_URL)
    if SFDC_SANDBOX == 'True':
        sf = Salesforce(instance_url=SFDC_INSTANCE_URL, client_id='mlsfdc',
                        username=SFDC_USERNAME, domain='test', password=SFDC_PASSWORD, security_token=SFDC_SECURITY_TOKEN)
    else:
        sf = Salesforce(instance_url=SFDC_INSTANCE_URL, client_id='mlsfdc',
                        username=SFDC_USERNAME, password=SFDC_PASSWORD, security_token=SFDC_SECURITY_TOKEN)

    return sf


class SalesforceConnection:
    __instance = None

    def getInstance():
        if SalesforceConnection.__instance is None:
            SalesforceConnection()
        return SalesforceConnection.__instance

    def __init__(self):
        if SalesforceConnection.__instance is not None:
            raise Exception(
                "There can only be one Salesforce Connection. This class is a singleton!")
        else:
            try:
                SalesforceConnection.__instance = login()
            except SalesforceAuthenticationFailed as err:
                raise
            except Exception as exc:
                raise
