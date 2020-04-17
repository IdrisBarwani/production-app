from django import forms
from .models import WorkOrderLog, RouteAssociation

# OPERATION_CHOICES = [
#     ('i', 'IN'),
#     ('o', 'OUT'),
#     ('m', 'Missing'),
#     ('r', 'Rejected'),
# ]
class WorkOrderLogForm(forms.ModelForm):
    # operation = forms.ChoiceField(choices=OPERATION_CHOICES, required=True )
    # operation = forms.ModelChoiceField(queryset=WorkOrderLog.objects.filter(routing_id=RouteAssociation))
    # work_order_fk = forms.IntegerField(widget=forms.HiddenInput(), initial=pk)
    error_css_class = 'error'
    class Meta:
        model = WorkOrderLog
        fields = ['operation', 'quantity','routing_id','work_order_fk']

    # def __init__(self, *args, **kwargs):
    #     # user = kwargs.pop('user','')
    #     super(WorkOrderLogForm, self).__init__(*args, **kwargs)
    #     self.fields['routing_id']=forms.ModelChoiceField(queryset=RouteAssociation.objects.all())