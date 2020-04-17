from django.shortcuts import render

from .models import WorkOrder, WorkOrderLog
from .forms import WorkOrderLogForm
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.shortcuts import render


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

# class TrialView(generic.DetailView):
#     model = WorkOrderLog
#     template_name = 'manufac/trial.html'
#     queryset = WorkOrderLog.objects.all()

#     def get_object(self):
#         obj = super().get_object()
#         return obj
    
#     def get_queryset(self):
#         return WorkOrderLog.objects.all()
#     # return HttpResponse("Hello, You're at the Manufacturing App's Trial index Page.")

class LogUpdateView(generic.FormView):
    template_name = 'manufac/trial.html'
    # context_object_name = 'WorkOrderLog'
    form_class = WorkOrderLogForm
    # fields = ['operation', 'quantity']

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['wol_list'] = WorkOrderLog.objects.all()
    #     return context

    # wol = get_object_or_404(WorkOrderLog, pk=WorkOrderLog_id)
    # return render(request, 'manufac/trial.html', {'wol': wol})

def recieve_data(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = WorkOrderLogForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            work_order_fk = form.cleaned_data.get('work_order_fk')
            routing_id = form.cleaned_data.get('routing_id')
            operation = form.cleaned_data.get('operation')
            quantity = form.cleaned_data.get('quantity')
            wol = WorkOrderLog.create(work_order_fk=work_order_fk, routing_id=routing_id, operation=operation, quantity=quantity)
            return HttpResponseRedirect('/admin/manufac/workorderlog/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = WorkOrderLogForm()

    return render(request, 'name.html', {'form': form})