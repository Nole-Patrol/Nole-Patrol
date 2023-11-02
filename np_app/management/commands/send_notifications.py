from django.core.mail import send_mail
from django.conf import settings
from np_app.models import RegisteredUser

'''
Function Name: send_notification_emails()
Description: This function iterates through each email in the RegisteredUser
             model. For every email, if new breaches are found in the most
             recent API request for a user's email, this function creates a
             message with the new breach sources and sends the message in a
             notification email. If no new breaches are found, the function
             prints a message to the console indicating this.
Parameters: new_breach_sources - a list of new breach sources found in the
                                most recent API request for a user's email
Return Value: None
Author(s): Brian Arango, Caitlin Marie Grimes
Last Modified Date: 1 November 2023
Assumptions: 
    - The EmailFile model contains emails from breached databases.
    - The RegisteredUser model saves users who have registered for notifications.
    - Email settings in settings.py are correctly configured.
References: 
    - https://docs.djangoproject.com/en/4.2/topics/db/queries/
    - https://docs.djangoproject.com/en/4.2/topics/email/
'''
def send_notification_emails(user, new_breach_sources):
    # If no new breaches are found, print a message to the console and return.
    if len(new_breach_sources) == 0:
        print('No new breaches found for ' + user.email)
        return
    # If new breaches are found, send a notification email.
    else:
        print('Sending notification email to ' + user.email)
        # Create a message with the new breach sources.
        message = []
        message.append('Your email has recently been found in the following breaches:\n')
        for i in new_breach_sources:
            message.append(i + '\n')
        message.append('For a full list of breaches affecting your email address, ' + 
                    'please see our updated database of breached emails.')
        final_message = ''.join(message)
        print(final_message)
        # If new breaches are found in most recent API request for user's email,
        # send a notification email.
        send_mail(
            'Breach Notification',
            final_message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        print('Notification email sent successfully')
