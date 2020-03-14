from django.shortcuts import render

from .models import WorkOrderLog
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    return HttpResponse("Hello, You're at the Manufacturing App's index.")

def start(request, pk):
    if request.user.has_perm('WorkOrder.change_WorkOrder'):
        WorkOrder.objects.filter(pk = pk).update(status='s')
    response = "Work order %s successfully."
    # return HttpResponse(response % pk)
    return HttpResponseRedirect('/admin/manufac/workorder/')

def add_wol(request, pk):
    # print('------------------------------')
    # print(request.GET.get('quantity'))
    # print('------------------------------')
    # wol = WorkOrder.create(product_sku_id=12227, status='h')
    # wol = Pack.create(name='mongodblist', product_sku_id=8776, route_id=1)
    wol = WorkOrderLog.create(work_order_fk_id=pk, routing_id_id=11, operation='i', quantity=request.GET.get('quantity'))
    return HttpResponseRedirect('/admin/manufac/workorderlog/')
    # return HttpResponse("Hello")

def get_wol(request, pk):
    html = '''<form action="/%s/add_wol/">
        <label for="lname">Quantity:</label>
        <input type="text" id="quantity" name="quantity"><br><br>
        <input type="submit" value="add">
    </form>''' % pk
    return HttpResponse(html)
