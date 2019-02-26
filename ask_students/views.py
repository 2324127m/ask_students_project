from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    pass
    return render(request, 'ask_students/index.html', {})
