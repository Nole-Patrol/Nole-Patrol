from django.core.management.base import BaseCommand
from np_app.models import EmailFile
import requests

'''
Class Name: Command(BaseCommand)
Description: This class inherits from Django's BaseCommand class and contains
             the code to import data retrieved from the HIBP API into the 
             EmailFile model and the associated SQLite database.
Author(s): Caitlin Marie Grimes
Last Modified Date: 1 November 2023
Assumptions: For records to be successfully inserted into the database, we 
             assume a nullable password field.
References: N/A
'''
class Command(BaseCommand):
    #help = 'Import email data from .txt files in various directories'
    
    '''
    Function Name: handle(self, *args, **options)
    Description: This function contains the code to import data retrieved from the 
                 HIBP API into the EmailFile model and the associated SQLite database.
    Parameters: self, *args, **options
    Return Value: N/A
    Author(s): Caitlin Marie Grimes
    Last Modified Date: 1 November 2023
    Assumptions: For records to be successfully inserted into the database, we 
                 assume a nullable password field.
    References: N/A
    '''
    def handle(self, *args, **options):
        account = 'cgrim.wa@gmail.com'

        url = "https://haveibeenpwned.com/api/v3/breachedaccount/" + account
        hibp_api_key = '71113c7ccb05453fbeb9d79b1121b2ef'
        payload={}
        headers = {
            'hibp-api-key': str(hibp_api_key),
            'format': 'application/json',
            'timeout': '2.5',
            'HIBP': str(hibp_api_key),
        }
        print(url)
        response = requests.request("GET", url, headers=headers, data=payload)

        response_string = response.text
        #print(response_string)
        for i in response_string:
            response_string = response_string.replace(
                '"', "").replace(
                    '[', "").replace(']', "").replace(
                        '{', "").replace(
                            '}', "").replace(
                                'Name:', "")
        print(response_string)

        email_instances = []
        for source in response_string.split(','):
            print(source)
            # Create an instance of the EmailFile model and append to email_instances list.
            email_instances.append(EmailFile(name=account, password="NULL", source=source))
            
        # Bulk insert instances into the EmailFile model and SQLite database.
        EmailFile.objects.bulk_create(email_instances)