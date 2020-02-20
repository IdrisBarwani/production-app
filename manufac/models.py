import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

STATUS_CHOICES = [
    ('d', 'Draft'),
    ('r', 'Confirmed'),
    ('s', 'Started'),
    ('h', 'Halted'),
    ('x', 'Cancelled'),
    ('c', 'Completed'),
]

PRIORITY_CHOICES = [
    (1, 'Urgent'),
    (2, 'High'),
    (3, 'Medium'),
    (4, 'Low'),
    (5, 'Least'),
]

class WorkOrder(models.Model):
    product_sku_id = models.IntegerField() #tssdb sku id
    product_sku_img = models.ImageField(upload_to='manufac/', null=True, blank=True)
    #created_at = models.DateTimeField()
    #created_by = models.CharField(max_length=20)
    #updated_at = odels.DateTimeField()
    #updated_by = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='d', choices=STATUS_CHOICES) #ENUM. DRAFT, CONFIRMED, STARTED, HALTED, COMPLETED.
    priority = models.IntegerField(choices=PRIORITY_CHOICES) #ENUM. 1, 2, 3.
    # required_quantity = models.IntegerField() #user input.
    #available_quantity = models.IntegerField() #derived quantity. upon pack explosion
    #pending_quantity = models.IntegerField() #derived quantity. required - available = pending
    start_time = models.DateTimeField(null=True, blank=True) #not shown to user . set using status.
    end_time = models.DateTimeField(null=True, blank=True) #not shown to user. set using status.
    # pack_component_sku = models.ForeignKey('TechPackSku', on_delete=models.CASCADE, null=True) # ---------Created to fetch values from TechPackSku Model

    def required_quantity(self):
        retrieval = ""
        required_quantity = Size.objects.filter(work_order_fk = self.id)
        for e in required_quantity:
            retrieval = e.total
        return retrieval

    def fabric_required(self):
        pack_lines = TechPackSku.objects.filter(work_order_id = self.id)
        retrieval = ""
        iteration = ""
        prevention = self.required_quantity()
        if prevention == '': prevention = 0 #---------------------------To prevent string values
        # print(
        #     type(hello)
        # )
        for e in pack_lines:
            retrieval = (
                int(prevention) * float(e.avg_consumption)
                )
            iteration = iteration + str(retrieval) + 'kg' + ' | '
        return iteration

    def avg_fabric_consumption(self):
        pack_lines = TechPackSku.objects.filter(work_order_id = self.id)
        retrieval = ""
        for e in pack_lines:
            fabric_sku_id = str(e.fabric_sku_id.id)
            fabric_sku_id_name = str(e.fabric_sku_id.name)
            retrieval = (retrieval 
                        + str(fabric_sku_id) + ' - ' + str(fabric_sku_id_name)
                        + ' -> ' 
                        + str(e.avg_consumption) + ' | ')
        return retrieval
 
class Pack(models.Model):
	#id field.
    #work_order = models.ForeignKey('WorkOrder', on_delete=models.CASCADE) #NOT REQUIRED.
    name = models.CharField(max_length=20)
    product_sku_id = models.IntegerField() #tssdb sku id
    def __str__(self):
        id_name = str(self.name) + ' - ' + str(self.product_sku_id)
        return id_name
 
class TechPackSku(models.Model):
    pack_id = models.ForeignKey('Pack', on_delete=models.CASCADE)
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
    #     name = TechPackSku.objects.filter(fabric_sku_id = self.id)
    #     retval = ""
    #     for i in name:
    #         retval = retval + str(self.id) + ' - ' + str(self.name) + ' '
    #     return retval
 
class InventoryTransaction(models.Model):
    component_sku_id = models.ForeignKey('ComponentSku', on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=10) #it'll be ENUM. ADD, SUBTRACT, RESERVED, UNRESERVED
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    #updated_by = models.CharField(max_length=20) #Either User or WorkOrder.

class Size(models.Model):
    work_order_fk = models.ForeignKey('WorkOrder', on_delete=models.CASCADE)
    XXS = models.PositiveIntegerField(default=0)
    XS = models.PositiveIntegerField(default=0)
    S = models.PositiveIntegerField(default=0)
    M = models.PositiveIntegerField(default=0)
    L = models.PositiveIntegerField(default=0)
    XL = models.PositiveIntegerField(default=0)
    XXL = models.PositiveIntegerField(default=0)
    @property
    def total(self):
        tolal = int(self.XXS) + int(self.XS) + int(self.S) + int(self.M) + int(self.L) + int(self.XL) + int(self.XXL)
        return tolal
    
# class Sort(models.Model):
#     work_order_fk = models.ForeignKey('WorkOrder', on_delete=models.CASCADE)
#     rejected = models.PositiveIntegerField(default=0)
#     missing = models.PositiveIntegerField(default=0)

#     def required_status(self):
#         retrieval = self.work_order_fk
#         print(retrieval)
#         # required_status = WorkOrder.objects.filter(id = self.work_order_fk)
#         # for e in required_status:
#         #     retrieval = e.status
#         # return required_status
