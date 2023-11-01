'''
Description: This script creates the base html for the breach cards. It takes
             input from the breaches.csv file and creates a card for each
             breach source and number of breached records. The html for each
             card is inserted into the breach_cards.html file.
'''
from jinja2 import Template
from django.core.management.base import BaseCommand
import csv
import os

file_path = 'np_app/Database/breaches.csv'

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        if os.path.isfile(file_path):
            cards = []
            breach_source = ""
            breached_records = ""
            # Open file and iterate through each line.
            with open(file_path, mode = 'r') as file:
                csvFile = csv.reader(file)
                for line in csvFile:
                    breach_source = line[0]
                    breached_records = line[1]
                    
                    template = Template('''
                        <div class="card">
                            <div class="card_text">
                                {{breach_source}}
                                {{breached_records}}<br>
                                Breaches
                            </div>
                        </div>
                    ''')

                    data = {
                        'breach_source': breach_source,
                        'breached_records': breached_records
                    }

                    cards.append(template.render(data))

            with open('np_app/templates/breach_cards.html', 'r+') as file:
                contents = file.readlines()
                # Insert cards into file.
                i = 0
                while i < len(cards):
                    contents.insert(22, cards[i])
                    file.seek(0)
                    i += 1
                    
                file.writelines(contents)