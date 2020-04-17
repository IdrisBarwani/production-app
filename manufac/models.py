import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group

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

PROCESS_CHOICES = [
    (1, 'Created'),
    (2, 'Confirmed'),
    (3, 'Cutting'),
    (4, 'Sorting'),
    (5, 'Printing'),
    (6, 'Stitching'),
    (7, 'Quality_Check'),
    (8, 'Packing'),
    (9, 'Completed'),
]

OPERATION_CHOICES = [
    ('i', 'IN'),
    ('o', 'OUT'),
    ('m', 'Missing'),
    ('r', 'Rejected'),
]

class Routing(models.Model):
    name = models.CharField(max_length=20)
    is_active = models.BooleanField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class RoutingGroup(models.Model):
    name = models.CharField(max_length=20)
    Routing = models.ManyToManyField('Routing', through='RouteAssociation')

    def __str__(self):
        return self.name  

def increment():

    print('_____________________________________________')

    red = RoutingGroup.objects.all()
    # hello = RoutingGroup.objects.latest('name')
    green = RouteAssociation.objects.all()
    for fetch in red:
        tino = fetch.name

        count = 0
        for fetch in green:
            purple = fetch.RoutingGroup
            maroon = str(purple)

            if (maroon == tino):
                count = count+1

    black = count+1


    print('_____________________________________________')


    return black

class RouteAssociation(models.Model):
    Routing = models.ForeignKey('Routing', on_delete=models.CASCADE)
    RoutingGroup = models.ForeignKey('RoutingGroup', on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=increment)
    
    def __str__(self):
        return (str(self.Routing) + ' -> ' + str(self.RoutingGroup))

class WorkOrder(models.Model):
    product_sku_id = models.IntegerField() #tssdb sku id
    product_sku_img = models.ImageField(upload_to='manufac/', null=True, blank=True)
    #created_at = models.DateTimeField()
    #created_by = models.CharField(max_length=20)
    #updated_at = odels.DateTimeField()
    #updated_by = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='d', choices=STATUS_CHOICES) #ENUM. DRAFT, CONFIRMED, STARTED, HALTED, COMPLETED.
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=3) #ENUM. 1, 2, 3.
    process = models.IntegerField(default=1, choices=PROCESS_CHOICES) #Current process of the work_order
    # required_quantity = models.IntegerField() #user input.
    #available_quantity = models.IntegerField() #derived quantity. upon pack explosion
    #pending_quantity = models.IntegerField() #derived quantity. required - available = pending
    start_time = models.DateTimeField(null=True, blank=True) #not shown to user . set using status.
    end_time = models.DateTimeField(null=True, blank=True) #not shown to user. set using status.
    # pack_component_sku = models.ForeignKey('TechPackSku', on_delete=models.CASCADE, null=True) # ---------Created to fetch values from TechPackSku Model
    # size_fk = models.ForeignKey('Size', on_delete=models.CASCADE, null=True, blank=True)
    sort_fk = models.ForeignKey('Sort', on_delete=models.CASCADE, null=True, blank=True)

    def missing(self):
        retrieval = ""
        required_quantity = Sort.objects.filter(work_order_fk = self.id)
        for e in required_quantity:
            retrieval = e.missing
        return retrieval

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

    def position_retrival(self):
        techPackSku = TechPackSku.objects.filter(work_order_id = self.id)
        for e in techPackSku:
            pack_id = e.pack_id.id
            pack = Pack.objects.filter(id = pack_id)
            for m in pack:
                route = m.route
                route_assc = RouteAssociation.objects.filter(RoutingGroup = route)
                for i in route_assc:
                    position = i.position
                    # print(position)
        # techPackSku12 = TechPackSku.objects.filter(work_order_id = self.id)        

class WorkOrderLog(models.Model):
    work_order_fk = models.ForeignKey('WorkOrder', on_delete=models.CASCADE)
    routing_id = models.ForeignKey('RouteAssociation', on_delete=models.CASCADE)
    operation = models.CharField(max_length=120, choices=OPERATION_CHOICES)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.operation

    def status(self):
        return self.quantity

    @classmethod
    def create(cls, work_order_fk, routing_id, operation, quantity):
        wol = cls(work_order_fk=work_order_fk, routing_id=routing_id, operation=operation, quantity=quantity)
        wol.save()
        return wol

class Pack(models.Model):
	#id field.
    #work_order = models.ForeignKey('WorkOrder', on_delete=models.CASCADE) #NOT REQUIRED.
    name = models.CharField(max_length=20)
    product_sku_id = models.IntegerField() #tssdb sku id
    route = models.ForeignKey('RoutingGroup', on_delete=models.CASCADE)   #which group of routes to be followed by product process

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
    
class Sort(models.Model):
    work_order_fk = models.ForeignKey('WorkOrder', on_delete=models.CASCADE)
    rejected = models.PositiveIntegerField(default=0)
    missing = models.PositiveIntegerField(default=0)
    # Sizes
    XXS = models.PositiveIntegerField(default=0)
    XS = models.PositiveIntegerField(default=0)
    S = models.PositiveIntegerField(default=0)
    M = models.PositiveIntegerField(default=0)
    L = models.PositiveIntegerField(default=0)
    XL = models.PositiveIntegerField(default=0)
    XXL = models.PositiveIntegerField(default=0)
    # To find total
    @property
    def total(self):
        tolal = int(self.XXS) + int(self.XS) + int(self.S) + int(self.M) + int(self.L) + int(self.XL) + int(self.XXL)
        return tolal

