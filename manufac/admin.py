import re
from django.contrib import admin
from django.utils.html import mark_safe,format_html


# Register your models here.

from .models import WorkOrder, Bom, BomComponentSku, ComponentSku, InventoryTransaction

class BomComponentSkuInline(admin.StackedInline):
    model = BomComponentSku
    extra = 1

class WorkOrderAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None,               {'fields': ['question_text']}),
    #     ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    # ]
    # inlines = [ChoiceInline]
    list_display = ('WorkOrder_id','product_sku_id', 'product_image', 'status','priority','required_quantity','avg_consumption_view','max_quantity_possible')
    inlines = [
        BomComponentSkuInline,
    ]
    def avg_consumption_view(self, obj):
        return obj.fabric_required()
    avg_consumption_view.short_description = "Fabric Consumption"
    avg_consumption_view.empty_value_display = '???'

    def max_quantity_possible(self, obj):
        max_quantity =  int(obj.required_quantity) * float(re.findall('\d*\.?\d+',str(obj.bom_component_sku))[1]);
        # return max_quantity
        return obj.get_required_quant()
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


# admin.site.register(WorkOrder)
admin.site.register(Bom)

class BomComponentSkuAdmin(admin.ModelAdmin):
    list_display = ('bom_id','avg_consumption','work_order_id','fabric_sku_id')

admin.site.register(BomComponentSku, BomComponentSkuAdmin)

class ComponentSkuAdmin(admin.ModelAdmin):
    list_display = ('id','name')

admin.site.register(ComponentSku, ComponentSkuAdmin)
admin.site.register(InventoryTransaction)