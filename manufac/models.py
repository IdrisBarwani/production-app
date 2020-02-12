import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

STATUS_CHOICES = [
    ('d', 'Draft'),
    ('r', 'Confirmed'),
    ('s', 'Started'),
    ('h', 'Halted'),
    ('c', 'Completed'),
]

PRIORITY_CHOICES = [
    (1, 'Urgent'),
    (2, 'High'),
    (3, 'Medium'),
    (4, 'Low'),
    (5, 'Least'),
]

# class BellManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(status='d')

class WorkOrder(models.Model):
    product_sku_id = models.IntegerField() #tssdb sku id
    product_sku_img = models.ImageField(upload_to='manufac/', null=True, blank=True)
    #created_at = models.DateTimeField()
    #created_by = models.CharField(max_length=20)
    #updated_at = odels.DateTimeField()
    #updated_by = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='d', choices=STATUS_CHOICES) #ENUM. DRAFT, CONFIRMED, STARTED, HALTED, COMPLETED.
    priority = models.IntegerField(choices=PRIORITY_CHOICES) #ENUM. 1, 2, 3.
    required_quantity = models.IntegerField() #user input.
    #available_quantity = models.IntegerField() #derived quantity. upon bom explosion
    #pending_quantity = models.IntegerField() #derived quantity. required - available = pending
    start_time = models.DateTimeField(null=True, blank=True) #not shown to user . set using status.
    end_time = models.DateTimeField(null=True, blank=True) #not shown to user. set using status.
    bom_component_sku = models.ForeignKey('BomComponentSku', on_delete=models.CASCADE, null=True) # ---------Created to fetch values from BomComponentSku Model

    def get_required_quant(self):
        bom_lines = BomComponentSku.objects.filter(work_order_id = self.id)
        retval = ""
        titan = ""
        for e in bom_lines:
            retval = (
                int(self.required_quantity) * float(e.avg_consumption)
                )
            titan = titan + str(retval) + 'kg' + ' | '
        return titan

    def fabric_required(self):
        bom_lines = BomComponentSku.objects.filter(work_order_id = self.id)
        retrieval = ""
        for e in bom_lines:
            fabric_sku_id = str(e.fabric_sku_id.id)
            fabric_sku_id_name = str(e.fabric_sku_id.name)
            retrieval = (retrieval 
                        + str(fabric_sku_id) + ' - ' + str(fabric_sku_id_name)
                        + ' -> ' 
                        + str(e.avg_consumption) + ' | ')
        return retrieval


    # people = BellManager()
    # def sometxt(self):
    #     return self.people.all()
 
class Bom(models.Model):
	#id field.
    #work_order = models.ForeignKey('WorkOrder', on_delete=models.CASCADE) #NOT REQUIRED.
    name = models.CharField(max_length=20)
    product_sku_id = models.IntegerField() #tssdb sku id
 
class BomComponentSku(models.Model):
    bom_id = models.ForeignKey('Bom', on_delete=models.CASCADE)
    fabric_sku_id = models.ForeignKey('ComponentSku', on_delete=models.CASCADE)
    work_order_id = models.ForeignKey('WorkOrder', on_delete=models.CASCADE, null=True, blank=True) #added to get this in inline view
    avg_consumption = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        id_name_consumption = str(self.fabric_sku_id) + ' -> ' + str(self.avg_consumption)
        return id_name_consumption
 
class ComponentSku(models.Model):
    #id = models.IntegerField()
    name = models.CharField(max_length=20) # fabric names.
    #quantity = models.DecimalField) #derived quantity using transaction table
    #reserved_qty = #derived quantity using transaction table
    def __str__(self):
        id_name = str(self.id) + ' - ' + self.name
        return id_name
    # def someref(self):
    #     name = BomComponentSku.objects.filter(fabric_sku_id = self.id)
    #     retval = ""
    #     for i in name:
    #         retval = retval + str(self.id) + ' - ' + str(self.name) + ' '
    #     return retval
 
class InventoryTransaction(models.Model):
    component_sku_id = models.ForeignKey('ComponentSku', on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=10) #it'll be ENUM. ADD, SUBTRACT, RESERVED, UNRESERVED
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    #updated_by = models.CharField(max_length=20) #Either User or WorkOrder.
