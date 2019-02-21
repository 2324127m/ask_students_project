from django.shortcuts import render


def index(request):
    pass
    return render(request, 'ask_students/index.html', {})
