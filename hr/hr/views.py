from django.shortcuts import render

def index(request):
    is_hr = request.user.groups.filter(name='hr').exists()
    context = {
        'is_hr': is_hr
    }
    return render(request, 'main/main.html', context)
