## Internal README for development
### apis.py
This script iterates through each registered user in the RegisteredUser model. For every user, it makes a request to the HIBP API for the user's email, isolates the breach sources from the response, and creates an instance of the EmailFile model for each breach source. If the source already exists for the user in the EmailFile table, the duplicate source is discarded. Finally, the new instances are bulk inserted into the EmailFile table, and the script calls the send_notification_emails() function in send_notifications.py to send a notification email for the new breaches. If no new breaches are found, no notification email is sent.

The script can be run by invoking
```sh
python manage.py apis
```
**Note:** The current version of apis.py must be run manually; future updates may see implementation of cron to enable scheduled runs which would enable automated API requests and email notifications.

### send_notifications.py
This script implements a function called send_notification_email(user, new_breach_sources) that takes two parameters: a user in the RegisteredUser model and a list of new breach sources. If new breaches are found in the most recent API request for a user's email (performed by apis.py), this function creates a message with the new breach sources and sends the message in a notification email. If no new breaches are found, the function prints a message to the console indicating this and no email is sent.

**Note:** This script is dependent on data from apis.py and should not be run independently.

### updatemodels.py
<!-- Description in progress - cmg -->
