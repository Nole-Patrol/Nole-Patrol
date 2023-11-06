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
'''
Class Name: PasswordGeneratorForm(forms.Form)
Description: This class inherits from Django's Form class and contains
             the code to create a form that allows users to search for
             email addresses in the database.
Author(s): Brian Arango.
Last Modified Date: 3 November 2023
Assumptions: N/A
References: N/A
'''
class PasswordGeneratorForm(forms.Form):
    include_lowercase = forms.BooleanField(label='Include Lowercase', required=False)
    include_uppercase = forms.BooleanField(label='Include Uppercase', required=False)
    include_numbers = forms.BooleanField(label='Include Numbers', required=False)
    include_special = forms.BooleanField(label='Include Special Characters', required=False)