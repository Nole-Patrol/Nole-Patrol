"""
Description: This file contains the code for the views of the np_app.
Author(s): Michael Sousa, Brian Arango, Caitlin Marie Grimes
Last Modified Date: 13 November 2023
Assumptions: N/A
References: https://docs.djangoproject.com/en/4.2/topics/http/views/
            https://docs.djangoproject.com/en/4.2/ref/request-response/
"""
import os
from django.shortcuts import render
from .forms import EmailSearchForm, PasswordSearchForm, PasswordGeneratorForm
from .models import EmailFile, RegisteredUser
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
import pwnedpasswords
import string
import random
from cryptography.hazmat.primitives.ciphers.aead import AESCCM

KEY = bytes.fromhex("59f055c39b5074dc7ea97abde24fc05a")
NONCE = bytes.fromhex("c2bad8b4a4536c8f0732e8c2be")
aesccm = AESCCM(KEY)


def set_password(password):
    """
    Encrypts the password and stores the ciphertext.
    """
    password = aesccm.encrypt(NONCE, password.encode(), None).hex()
    return password


"""
Function Name: index(request)
Description: This function contains the code to render the index.html page and
             process the user's email search query.
Parameters: request
Return Value: HTTPResponse
Author(s): Michael Sousa Jr., Caitlin Marie Grimes
Last Modified Date: 27 October 2023
Assumptions: N/A
References: https://docs.djangoproject.com/en/4.2/ref/request-response/
"""


def index(request):
    print("Request method:", request.method)  # Debugging statement

    if request.method == "POST":
        form = EmailSearchForm(request.POST)

        if form.is_valid():
            user_email = form.cleaned_data["email"]
            print("User email:", user_email)  # Debugging statement

            # Use Django's ORM to search for the email in the database.
            matching_records = EmailFile.objects.filter(name=user_email)
            print("Matching records:", matching_records)  # Debugging statement

            # If the email is found in the database, extract the distinct sources.
            if matching_records.exists():
                sources = set(record.source for record in matching_records)
                # Render the search.html page with the results.
                return render(
                    request,
                    "search.html",
                    {"user_email": user_email, "sources": sources},
                )
            else:
                print("No matching records for:", user_email)  # Debugging statement
                # Render the search.html page with the no_match flag set to True.
                return render(
                    request, "search.html", {"user_email": user_email, "no_match": True}
                )
        else:
            print("Form errors:", form.errors)  # Debugging statement

    else:
        form = EmailSearchForm()

    return render(request, "index.html", {"form": form})


def breaches_page(request):
    return render(request, "breaches.html")


def about_page(request):
    return render(request, "about.html")


def password_page(request):
    return render(request, "password.html")


def passgen_page(request):
    return render(request, "passgen.html")


"""
Function Name: notify_page(request)
Description: This function handles the process of notifying users if their email is found in the breached 
             database. On a POST request, it checks the EmailFile model for the provided email. If found,
             it sends a breach notification to the user's email. Additionally, the email is saved in the
             RegisteredUser model if not already present. After processing, it redirects to a success page.
             It also sends a thank you email as a confirmation, useful for testing purposes.
Parameters: request
Return Value: HTTPResponse
Author(s): Brian Arango
Last Modified Date: 30 October 2023
Assumptions: The EmailFile model contains emails from breached databases. The RegisteredUser model saves 
             users who have been notified.
References: https://docs.djangoproject.com/en/4.2/ref/request-response/, 
            https://docs.djangoproject.com/en/4.2/topics/email/#
"""


def notify_page(request):
    if request.method == "POST":
        email = request.POST.get("email")

        # Check if the email exists in the EmailFile model.
        exists_in_breach = EmailFile.objects.filter(name=email).exists()

        # If it exists in the breach, send a notification email to the user.
        breach_message = (
            "Your email has been found in our database of breached emails.\n"
            + "For a full list of past breaches affecting your email address, "
            + "please see our database. We will notify you if your email is found in any future breaches."
        )
        if exists_in_breach:
            send_mail(
                "Breach Notification",
                breach_message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

        # Save the email in the RegisteredUser model if it's not already there.
        created = RegisteredUser.objects.get_or_create(email=email)

        # If the user is newly registered (i.e., email was just added), send a thank you email.
        if created:
            send_mail(
                "Thank you for registering for Nole Patrol breach notifications",
                "Thank you for registering for email breach notifications. We will notify you if your email is found in any future breaches.",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

        # Redirect to a success page or display a success message (based on your design).
        return HttpResponseRedirect(
            "/success/"
        )  # Change this URL based on your design.

    return render(request, "notify.html")


def success_view(request):
    return render(request, "success.html")


"""
Function Name: password_page(request)
Description: This function contains the code to render the password.html page
             and process the user's password search query.
Parameters: request
Return Value: HTTPResponse
Author(s): Caitlin Marie Grimes
Last Modified Date: 14 November 2023
Assumptions: N/A
References: https://docs.djangoproject.com/en/4.2/ref/request-response/
"""


def password_page(request):
    if request.method == "POST":
        form = PasswordSearchForm(request.POST)

        if form.is_valid():
            cleartext_password = form.cleaned_data["password"]
            print("Password:", cleartext_password)  # Debugging statement
            # Use Django's ORM to search for the password in the database.
            encrypted_password = set_password(cleartext_password)
            print("Encrypted Password:", encrypted_password)
            matching_records = EmailFile.objects.filter(password=encrypted_password)
            print(matching_records)

            # If the password is found in the database or API, return true.
            if matching_records.exists() or pwnedpasswords.check(cleartext_password):
                # Render the search.html page with the results.
                return render(request, "search.html", {"password": cleartext_password})
            else:
                print(
                    "No matching records for:", cleartext_password
                )  # Debugging statement
                # Render the search.html page with the no_match flag set to True.
                return render(
                    request,
                    "search.html",
                    {"password": cleartext_password, "no_match": True},
                )
        else:
            print("Form errors:", form.errors)  # Debugging statement

    else:
        form = PasswordSearchForm()

    return render(request, "password.html", {"form": form})


"""
Function Name: passgen_page(request)
Description: This function handles the rendering of the passgen.html page and the
             generation of passwords based on user preferences. Upon a POST request,
             it processes the submitted PasswordGeneratorForm to generate a random password
             according to the specified criteria (lowercase, uppercase, numbers, and special characters).
             If no options are selected, it prompts the user to select at least one option.
             The generated password, if any, is then displayed on the passgen.html page.
Parameters: request
Return Value: HTTPResponse
Author(s): Brian Arango
Last Modified Date: 15 November 2023
Assumptions: N/A
References: https://docs.djangoproject.com/en/4.2/ref/request-response/
"""


def passgen_page(request):
    generated_password = None

    if request.method == "POST":
        form = PasswordGeneratorForm(request.POST)
        if form.is_valid():
            # Extracting choices from the form
            include_lowercase = form.cleaned_data["include_lowercase"]
            include_uppercase = form.cleaned_data["include_uppercase"]
            include_numbers = form.cleaned_data["include_numbers"]
            include_special = form.cleaned_data["include_special"]
            password_length = form.cleaned_data[
                "password_length"
            ]  # Extracting the password length

            # Building the character set based on choices
            characters = ""
            if include_lowercase:
                characters += string.ascii_lowercase
            if include_uppercase:
                characters += string.ascii_uppercase
            if include_numbers:
                characters += string.digits
            if include_special:
                characters += string.punctuation

            # Generating the password
            if characters:
                generated_password = "".join(
                    random.choice(characters) for i in range(password_length)
                )
            else:
                generated_password = "Please select at least one option."

    else:
        form = PasswordGeneratorForm()

    return render(
        request,
        "passgen.html",
        {"form": form, "generated_password": generated_password},
    )
