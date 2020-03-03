import re
from django.contrib import admin
from django.utils.html import mark_safe,format_html
from django.contrib.auth.models import User, Group


# Register your models here.

from .models import WorkOrder, Pack, TechPackSku, ComponentSku, InventoryTransaction, Size, Sort, WorkOrderLog, Routing, RouteAssociation, RoutingGroup

class TechPackSkuInline(admin.StackedInline):
    model = TechPackSku
    extra = 1
    verbose_name = 'Fabric'
    verbose_name_plural = 'Fabric'

class SizeInline(admin.StackedInline):
    model = Size
    # readonly_fields = ('XXL','total')
    max_num = 1

class WorkOrderAdmin(admin.ModelAdmin):
    # print('-------start----------')
    # # for e in User.objects.all():        ----------- Use this code to fetch all users
    # #     print(e)
    # # all_fields = User._meta.get_fields()
    # print('-------stop----------')
    
    list_display = ['WorkOrder_id','product_sku_id', 'product_image', 'status','priority','process','required_quantity','avg_fabric_consumption','fabric_required','action_button']

    fields = ('product_sku_id','status','priority')

    def get_list_display(self, request):
        current_user_username = request.user.get_username()
        users_in_cutting_group = Group.objects.get(name="cutting").user_set.all()
        users_in_sorting_group = Group.objects.get(name="sorting").user_set.all()

        for fetch in users_in_cutting_group:
            cutting_users_username = str(fetch)
            print(cutting_users_username)
            if cutting_users_username == current_user_username:
                print('hurray!')
                if 'action_button' in self.list_display:
                    self.list_display.remove('action_button')      
                else:
                    self.list_display.append('action_button')
                    print('nope buddy :(')

        for fetch in users_in_sorting_group:
            sorting_users_username = str(fetch)
            print(sorting_users_username)
            if sorting_users_username == current_user_username:
                print('hurray!')
                if 'action_button' in self.list_display:
                    self.list_display.remove('action_button')
                if 'avg_fabric_consumption' in self.list_display:
                    self.list_display.remove('avg_fabric_consumption')
                if 'fabric_required' in self.list_display:
                    self.list_display.remove('fabric_required')
                else:
                    self.list_display.append('avg_fabric_consumption')
                    self.list_display.append('fabric_required')
                    self.list_display.append('action_button')
                    print('nope buddy :(')

        return self.list_display

    def get_queryset(self, request):
        current_user_username = request.user.get_username()
        users_in_cutting_group = Group.objects.get(name="cutting").user_set.all()
        for fetch in users_in_cutting_group:
            cutting_users_username = str(fetch)
            queryset = super(WorkOrderAdmin, self).get_queryset(request)
            if cutting_users_username == current_user_username:
                queryset = super(WorkOrderAdmin, self).get_queryset(request)
                queryset = queryset.filter(process=3)
            return queryset
        

    inlines = [
        TechPackSkuInline, SizeInline
    ]

    def fabric_required(self, obj): #---------------------This block of code can be removed later
        # max_quantity =  int(obj.required_quantity) * float(re.findall('\d*\.?\d+',str(obj.pack_component_sku))[1]);
        return obj.fabric_required()
    fabric_required.short_description = "Fabric Required"
    fabric_required.empty_value_display = '???'

    list_filter = ['status','priority','process']
    list_editable = ('priority',)
    # search_fields = ['product_sku_id']
    # list_per_page = 1
    actions = ['make_confirm','make_start']

    def action_button(self, obj):
        # Use this to check for self and then update the status
        # WorkOrder.objects.update(status='c')
        # print(WorkOrder.objects.filter(id=obj.pk))
        # white = format_html('<button id="%(id)s" data-value="%(value)s">Completed</button>' % {'id': obj.pk, 'value': obj.status})
        black = format_html('<a class="button" href="/%(id)s/start">Mark Started</a>'% {'id': obj.pk})
        return black
    action_button.short_description = "Change status"

    def WorkOrder_id(self, obj):
        return obj.id
    WorkOrder_id.short_description = "Work Order ID"

    def make_confirm(self, request, queryset):
        rows_updated = queryset.update(status='r')
        if rows_updated == 1:
            message_bit = "1 Work-Order was"
        else:
            message_bit = "%s Work-Orders were" % rows_updated
        self.message_user(request, "%s successfully marked as Confirmed." % message_bit)
    make_confirm.short_description = "Mark selected Work-Orders as Confirmed"

    def make_start(self, request, queryset):
        queryset.update(status='s')
    make_start.short_description = "Mark selected Work-Orders as Started"

    def product_image(self, obj):
        return mark_safe('<img src="https://images.thesouledstore.com/public/theSoul/uploads/catalog/product/20200127175234-1.jpg" width="{width}" height={height} />'.format(
            url = obj.product_sku_img,
            width=80,
            height=80,
            )
    )
    # def product_image(self, obj):
    #     return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
    #         url = obj.product_sku_img,
    #         width=80,
    #         height=80,
    #         )
    # )

admin.site.register(WorkOrder, WorkOrderAdmin)


class PackAdmin(admin.ModelAdmin):
    list_display = ('name','product_sku_id')
admin.site.register(Pack, PackAdmin)

class TechPackSkuAdmin(admin.ModelAdmin):
    list_display = ('pack_id','avg_consumption','work_order_id','fabric_sku_id')

admin.site.register(TechPackSku, TechPackSkuAdmin)

class ComponentSkuAdmin(admin.ModelAdmin):
    list_display = ('id','name')

admin.site.register(ComponentSku, ComponentSkuAdmin)
admin.site.register(InventoryTransaction)

class SizeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Size._meta.get_fields()]
    
    # readonly_fields = ('XXS','total_m')
    # fields = ('XXS','XS','S','M','L','XL','XXL','total_m')
    # list_display = ('XXS','XS','S','M','L','XL','XXL','total_m')
    # def total_m(self, obj):
    #     tol = int(obj.S) + int(obj.M);
    #     return tol
admin.site.register(Size, SizeAdmin)

class SortAdmin(admin.ModelAdmin):
    list_display = ('rejected','missing','XXS','XS','S','M','L','XL','XXL','total')

admin.site.register(Sort, SortAdmin)

class LogAdmin(admin.ModelAdmin):
    list_display = [field.name for field in WorkOrderLog._meta.get_fields()]

admin.site.register(WorkOrderLog, LogAdmin)

class RoutingAdmin(admin.ModelAdmin):
    list_display = ['name','is_active']

admin.site.register(Routing, RoutingAdmin)

class RoutingGroupAdmin(admin.ModelAdmin):
    list_display = ['name',]

admin.site.register(RoutingGroup, RoutingGroupAdmin)

class RouteAssociationAdmin(admin.ModelAdmin):
    list_display = ['Routing','RoutingGroup','position']

admin.site.register(RouteAssociation, RouteAssociationAdmin)
