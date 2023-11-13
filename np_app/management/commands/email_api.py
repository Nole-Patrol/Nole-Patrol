from django.core.management.base import BaseCommand
from np_app.models import EmailFile, RegisteredUser
from np_app.management.commands.send_notifications import send_notification_emails
import requests
import time

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
    '''
    Function Name: handle(self, *args, **options)
    Description: This function iterates through each registered user in the
                 RegisteredUser model. For every user, this function makes a
                 request to the HIBP API for the user's email, saves the response
                 as a string and removes unnecessary characters from the response
                 string to isolate the breach sources. The function creates an
                 instance of the EmailFile model for each breach source. If the
                 source already exists for the user in the EmailFile table, the 
                 duplicate source is discarded. Finally, the new instances are
                 bulk inserted into the EmailFile table, and the function calls
                 the send_notification_emails() function in send_notifications.py
                 to send a notification email for the new breaches. If no new
                 breaches are found, no notification email is sent.
    Parameters: self, *args, **options
    Return Value: N/A
    Author(s): Caitlin Marie Grimes
    Last Modified Date: 1 November 2023
    Assumptions: For records to be successfully inserted into the database, we 
                 assume a nullable password field.
    References: N/A
    Notes: The HIBP API has a rate limit of 10 requests per minute. To avoid
           exceeding the rate limit, this function sleeps for 6 seconds after
           each request.
    '''
    def handle(self, *args, **options):
        # Get all registered users from the RegisteredUser table.
        registered_users = RegisteredUser.objects.all()
        user_count = 0
        # Get the count of registered users.
        for user in registered_users:
            user_count += 1
        current_user = 0
        # Iterate through each registered user.
        for user in registered_users:
            current_user += 1
            # Make a request to the HIBP API for the current user.
            url = "https://haveibeenpwned.com/api/v3/breachedaccount/" + str(user)
            hibp_api_key = '71113c7ccb05453fbeb9d79b1121b2ef'
            payload={}
            headers = {
                'hibp-api-key': str(hibp_api_key),
                'format': 'application/json',
                'timeout': '2.5',
                'HIBP': str(hibp_api_key),
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            # Save the response as a string.
            response_string = response.text
            # Remove unnecessary characters from the response string to isolate
            # the breach sources.
            for i in response_string:
                response_string = response_string.replace(
                    '"', "").replace(
                        '[', "").replace(']', "").replace(
                            '{', "").replace(
                                '}', "").replace(
                                    'Name:', "")
            
            email_instances = []
            # Iterate through the response string to create an instance of the
            # EmailFile model for each breach source. Add each instance to the
            # email_instances list.
            for source in response_string.split(','):
                email_instances.append(EmailFile(name=user, password="NULL", source=source))
            
            new_email_instances = []
            new_breach_sources = []
            # Check if the source already exists for this user in the EmailFile table.
            for instance in email_instances:
                if EmailFile.objects.filter(name=instance.name, 
                                            source=instance.source).exists() == False:
                    # If the source does not exist for this user,
                    # add the instance to the new_email_instances list,
                    # add the source to new_breach_sources.
                    new_email_instances.append(instance)
                    new_breach_sources.append(instance.source)
            # Bulk insert new instances into the EmailFile table.
            EmailFile.objects.bulk_create(new_email_instances)
            # If new breaches are found in most recent API request for user's email,
            # send a notification email.
            send_notification_emails(user, new_breach_sources)
            print("Updates for user " + str(current_user) + " of " + str(user_count) + " complete.")
            # Sleep for 6 seconds to avoid exceeding the rate limit.
            time.sleep(6)