from django.shortcuts import render
from django.conf import settings
import csv
import json
from pathlib import Path
#from django.http import HttpResponse


def index(request):
    data = {
        'title': 'Main Page',
        'values': ['Some', 'Hello', '123']
    }
    return render(request, 'main/index.html', data)


def about(request):
    return render(request, 'main/about.html')


#def csv_table(request):
#    csv_file_path = Path(settings.BASE_DIR) / 'static' / 'csv' / 'lp_state_protectorate.csv'
#    with open(csv_file_path, 'r') as file:
#        csv_reader = csv.reader(file)
#        table = list(csv_reader)

#    creation_date = table[-1][0]

#    context = {
#        'table': table,
#        'creation_date': creation_date,
#    }

#    return render(request, 'main/table.html', context)


def csv_table(request):
    csv_file_path = Path(settings.BASE_DIR) / 'static' / 'json' / 'lp_state_protectorate.json'
    with open(csv_file_path, 'r') as file:
        table = json.load(file)

#    creation_date = table[]

    context = {
        'table': table,
#        'creation_date': creation_date,
    }
    return render(request, 'main/table.html', context)
