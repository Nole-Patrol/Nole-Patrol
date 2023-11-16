"""
Description: This file contains the code for the EmailSearchForm and
             PasswordSearchForm classes. These classes are used to 
             create forms that allows users to search the database
             and linked APIs for email addresses and passwords, 
             respectively.
Author(s): Michael Sousa Jr., Caitlin Marie Grimes
Last Modified Date: 13 November 2023
Assumptions: N/A
References: https://docs.djangoproject.com/en/4.2/topics/forms/
"""
from django import forms

"""
Class Name: EmailSearchForm(forms.Form)
Description: This class inherits from Django's Form class and contains
             the code to create a form that allows users to search for
             email addresses in the database.
Author(s): Michael Sousa Jr.
Last Modified Date: 27 October 2023
Assumptions: N/A
References: https://docs.djangoproject.com/en/4.2/topics/forms/
"""


class EmailSearchForm(forms.Form):
    email = forms.EmailField(label="Email")


"""
Class Name: PasswordSearchForm(forms.Form)
Description: This class inherits from Django's Form class and contains
             the code to create a form that allows users to search for
             passwords in the database.
Author(s): Caitlin Marie Grimes
Last Modified Date: 13 November 2023
Assumptions: N/A
References: https://docs.djangoproject.com/en/4.2/topics/forms/
"""


class PasswordSearchForm(forms.Form):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


"""
Class Name: PasswordGeneratorForm(forms.Form)
Description: Creates passwords. Has booleans for including lowercase, uppercase, numbers, and special characters.
Author(s): Brian Arango.
Last Modified Date: 3 November 2023
Assumptions: N/A
References: N/A
"""


class PasswordGeneratorForm(forms.Form):
    include_lowercase = forms.BooleanField(label="Include Lowercase", required=False)
    include_uppercase = forms.BooleanField(label="Include Uppercase", required=False)
    include_numbers = forms.BooleanField(label="Include Numbers", required=False)
    include_special = forms.BooleanField(
        label="Include Special Characters", required=False
    )
    password_length = forms.IntegerField(
        label="Password Length", min_value=6, max_value=20, initial=12
    )
