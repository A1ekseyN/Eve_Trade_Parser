#from django.conf import settings
#import csv
#from django.shortcuts import render
#import os

#def csv_table(request):
#    csv_file_path = os.path.join(settings.BASE_DIR, 'static', 'csv', 'lp_state_protectorate.csv')
#    with open(csv_file_path, 'r') as file:
#        csv_reader = csv.reader(file)
#        table = list(csv_reader)
#    return render(request, 'main/state_protectorate.html', {'table': table})



