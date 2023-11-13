from django.test import TestCase, Client
from .models import EmailFile, RegisteredUser
from django.db import IntegrityError
from django.urls import reverse
from .forms import EmailSearchForm
from django.core import mail

'''1-models.py test'''
class EmailFileTestCase(TestCase):
    def setUp(self):
        # Set up data for testing
        self.email_file = EmailFile.objects.create(
            name="TestUser",
            source="TestSource",
            password="TestPassword"
        )

    def test_encrypt_decrypt_password(self):
        # Test encryption and decryption of passwords
        password = "TestPassword"
        encrypted_password = self.email_file.encrypt_password(password)
        decrypted_password = self.email_file.decrypt_password(encrypted_password)
        self.assertEqual(password, decrypted_password)

    def test_email_file_str_method(self):
        # Test the __str__ method of EmailFile model
        expected_str = "TestUser"
        self.assertEqual(str(self.email_file), expected_str)

class RegisteredUserTestCase(TestCase):
    def setUp(self):
        # Set up data for testing RegisteredUser model
        self.registered_user = RegisteredUser.objects.create(
            email="test@example.com"
        )

    def test_registered_user_str_method(self):
        # Test the __str__ method of RegisteredUser model
        expected_str = "test@example.com"
        self.assertEqual(str(self.registered_user), expected_str)

    def test_unique_email_constraint(self):
        # Test that email field in RegisteredUser model is unique
        duplicate_user = RegisteredUser(email="test@example.com")
        with self.assertRaises(IntegrityError):
            duplicate_user.save()

'''2-Search Functionality test'''
class EmailSearchFormTest(TestCase):
    def setUp(self):
        # Create a test database record
        self.email_address = 'test@example.com'
        RegisteredUser.objects.create(email=self.email_address)
    def test_valid_form(self):
        # Test with a valid email address
        form_data = {'email': 'testapp@fsu.edu'}
        form = EmailSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Test with an invalid email address
        form_data = {'email': 'test@'}
        form = EmailSearchForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_empty_form(self):
        # Test with an empty form
        form = EmailSearchForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['This field is required.'])

    def test_valid_search(self):
        # Test searching with an email that is present in the database
        form_data = {'email': self.email_address}
        form = EmailSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Simulate how the form is used in a view or other context
        # For example, you might use the form's cleaned_data to filter your queryset
        search_results = RegisteredUser.objects.filter(email=form.cleaned_data['email'])

        # Assert that the search results contain the expected email address
        self.assertEqual(search_results.count(), 1)
        self.assertEqual(search_results[0].email, self.email_address)

    def test_invalid_search(self):
        # Test searching with an email that is not present in the database
        form_data = {'email': 'nonexistent@example.com'}
        form = EmailSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Simulate how the form is used in a view or other context
        # For example, you might use the form's cleaned_data to filter your queryset
        search_results = RegisteredUser.objects.filter(email=form.cleaned_data['email'])

        # Assert that the search results are empty
        self.assertEqual(search_results.count(), 0)

'''3-Navigation test'''

'''Ensure that the user can navigate to the Home page'''
class HomePageTest(TestCase):
    def test_home_page_access(self):
        # Simulate a GET request to the home URL
        response = self.client.get('/')

        # Assert that the response status code is 200 (OK) or 302 (redirect) if applicable
        self.assertIn(response.status_code, [200, 302])

        # If the response is a redirect, assert that the redirection is to the correct URL
        if response.status_code == 302:
            self.assertEqual(response.url, '/')

'''Ensure that the user can navigate to the About page'''
class AboutPageTest(TestCase):
    def test_about_page_access(self):
        # Simulate a GET request to the '/about/' URL
        response = self.client.get('/about/')

        # Assert that the response status code is 200 (OK) or 302 (redirect) if applicable
        self.assertIn(response.status_code, [200, 302])

        # If the response is a redirect, assert that the redirection is to the correct URL
        if response.status_code == 302:
            self.assertEqual(response.url, '/about/')

'''Ensure that the user can navigate to the Breaches page'''
class BreachesPageTest(TestCase):
    def test_breaches_page_access(self):
        # Simulate a GET request to the '/breaches/' URL
        response = self.client.get('/breaches/')

        # Assert that the response status code is 200 (OK) or 302 (redirect) if applicable
        self.assertIn(response.status_code, [200, 302])

        # If the response is a redirect, assert that the redirection is to the correct URL
        if response.status_code == 302:
            self.assertEqual(response.url, '/breaches/')

'''Ensure that the user can navigate to the Notify Me page'''
class NotifyMePageTest(TestCase):
    def test_notify_me_page_access(self):
        # Simulate a GET request to the '/notify/' URL
        response = self.client.get('/notify/')

        # Assert that the response status code is 200 (OK) or 302 (redirect) if applicable
        self.assertIn(response.status_code, [200, 302])

        # If the response is a redirect, assert that the redirection is to the correct URL
        if response.status_code == 302:
            self.assertEqual(response.url, '/notify/')


'''4-Email Notification Functionality test'''
class EmailNotificationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_for_email_notifications(self):
        # Step 1: Navigate to the signup page
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

        # Step 2: Enter a valid email address into the input field
        email_address = 'test@example.com'
        response = self.client.post(reverse('signup'), {'email': email_address})
        self.assertEqual(response.status_code, 302)  # Assuming a successful form submission redirects to success page

        # Step 3: Check the expected result
        # Check that the user is redirected to the success page
        self.assertRedirects(response, reverse('success'))

        # Check that the user is signed up in the database
        user_exists = RegisteredUser.objects.filter(email=email_address).exists()
        self.assertTrue(user_exists)

        # Check that the user receives an automated email confirmation
        self.assertEqual(len(mail.outbox), 1)  # Check that one email was sent
        self.assertEqual(mail.outbox[0].to, [email_address])  # Check that the email is sent to the correct address
        self.assertIn('Thank you for registering for Nole Patrol breach notifications', mail.outbox[0].subject)  # Check the email subject

