def lpstore(request):
    return render(request, 'lpstore/index.html')


def csv_table(request):
    csv_file_path = Path(settings.BASE_DIR) / 'static' / 'json' / 'lp_state_protectorate.json'
    with open(csv_file_path, 'r') as file:
        table = json.load(file)

#    creation_date = table[]

    context = {
        'state_protectorate': table,
#        'creation_date': creation_date,
    }
    return render(request, 'lpstore/state_protectorate.html', context)
