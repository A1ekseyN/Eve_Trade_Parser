from django.shortcuts import render
from django.conf import settings
import csv
import json
from pathlib import Path
#from django.http import HttpResponse


def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def lpstore(request):
    return render(request, 'lpstore/index.html')


def json_table(request):
    json_file_path = Path(settings.BASE_DIR) / 'static' / 'json' / 'lp_state_protectorate.json'
    with open(json_file_path, 'r') as file:
        table = json.load(file)

#    creation_date = table[]

    context = {
        'state_protectorate': table,
#        'creation_date': creation_date,
    }
    return render(request, 'lpstore/state_protectorate.html', context)
