from django.core.mail import send_mail
from django.conf import settings
from np_app.models import RegisteredUser, EmailFile

'''
Function Name: send_notification_emails()
Description: This function iterates through each email in the RegisteredUser model. For every email, it checks if 
             it exists in the EmailFile model, which contains breached email addresses. If a match is found, a 
             breach notification is sent to the registered user's email.
Parameters: None
Return Value: None
Author(s): Brian Arango
Last Modified Date: 30 October 2023
Assumptions: 
    - The EmailFile model contains emails from breached databases.
    - The RegisteredUser model saves users who have registered for notifications.
    - Email settings in settings.py are correctly configured.
References: 
    - https://docs.djangoproject.com/en/4.2/topics/db/queries/
    - https://docs.djangoproject.com/en/4.2/topics/email/
'''
def send_notification_emails():
    # Get all registered users
    registered_users = RegisteredUser.objects.all()

    for user in registered_users:
        # Check if the user's email exists in the EmailFile model
        exists_in_breach = EmailFile.objects.filter(name=user.email).exists()
        
        # If the email exists in the breach, send a notification email
        if exists_in_breach:
            send_mail(
                'Breach Notification',
                'Your email has been found in our updated database of breached emails.',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

if __name__ == "__main__":
    send_notification_emails()
