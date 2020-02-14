import re
from django.contrib import admin
from django.utils.html import mark_safe,format_html


# Register your models here.

from .models import WorkOrder, Pack, TechPackSku, ComponentSku, InventoryTransaction, Size

class TechPackSkuInline(admin.StackedInline):
    model = TechPackSku
    extra = 1

class SizeInline(admin.StackedInline):
    model = Size
    # readonly_fields = ('XXL','total')
    max_num = 1

class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ('WorkOrder_id','product_sku_id', 'product_image', 'status','priority','required_quantity','avg_consumption_view','max_quantity_possible')
    inlines = [
        TechPackSkuInline, SizeInline
    ]

    def required_quantity(self, obj):
        return obj.required_quantity()

    def avg_consumption_view(self, obj):
        return obj.fabric_required()
    avg_consumption_view.short_description = "Fabric Consumption"
    avg_consumption_view.empty_value_display = '???'

    def max_quantity_possible(self, obj):
        # max_quantity =  int(obj.required_quantity) * float(re.findall('\d*\.?\d+',str(obj.pack_component_sku))[1]);
        return obj.max_quantity_possible()
    max_quantity_possible.short_description = "Fabric Required"
    max_quantity_possible.empty_value_display = '???'

    list_filter = ['status','priority']
    # search_fields = ['product_sku_id']
    # list_per_page = 1
    actions = ['make_confirm','make_start']

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