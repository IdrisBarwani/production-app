from django.shortcuts import render

from .models import WorkOrder
# Create your views here.
from django.http import HttpResponseRedirect


def index(request):
    return HttpResponse("Hello, You're at the Manufacturing App's index.")

def start(request, pk):
    WorkOrder.objects.filter(pk = pk).update(status='s')
    response = "Work order %s successfully."
    # return HttpResponse(response % pk)
    return HttpResponseRedirect('/admin/manufac/workorder/')