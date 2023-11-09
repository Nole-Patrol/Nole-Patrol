'''
Description: This file contains the code for the EmailSearchForm class. This
             class is used to create a form that allows users to search for
             email addresses in the database.
Author(s): Michael Sousa Jr.
Last Modified Date: 27 October 2023
Assumptions: N/A
References: N/A
'''
from django import forms

'''
Class Name: EmailSearchForm(forms.Form)
Description: This class inherits from Django's Form class and contains
             the code to create a form that allows users to search for
             email addresses in the database.
Author(s): Michael Sousa Jr.
Last Modified Date: 27 October 2023
Assumptions: N/A
References: N/A
'''
class EmailSearchForm(forms.Form):
    email = forms.EmailField(label="Email")

class PasswordSearchForm(forms.Form):
    password = forms.CharField(label="Password")