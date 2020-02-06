from django.contrib import admin
from django.utils.html import mark_safe


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
    list_display = ('WorkOrder_id','product_sku_id', 'product_image', 'status','priority','required_quantity','avg_consumption_view')
    inlines = [
        BomComponentSkuInline,
    ]
    def avg_consumption_view(self, obj):
        # return obj.avg_consumption
        return obj
        avg_consumption_view.short_description = "AVG Order ID"
        avg_consumption_view.empty_value_display = '???'

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
admin.site.register(BomComponentSku)
admin.site.register(ComponentSku)
admin.site.register(InventoryTransaction)