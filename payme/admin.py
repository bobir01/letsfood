from django.contrib import admin

from payme.models import MerchatTransactionsModel
from payme.models import Orders
from payme.models import MenuLunch
from payme.models import MenuDinner


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'price', 'quantity', 'is_paid', 'event', 'menu_type',)
    list_filter = ('is_paid', 'order_time')
    search_fields = ('order_id',)


class MenuLunchAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'price_full', 'price_par', 'full_text_uz', 'full_text_ru', 'full_text_en', 'par_text_uz',
        'par_text_ru', 'par_text_en', 'image_tag')
    search_fields = ('id',)


class MenuDinnerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'price_full', 'price_par', 'full_text_uz', 'full_text_ru', 'full_text_en', 'par_text_uz',
        'par_text_ru', 'par_text_en', 'image_tag')
    search_fields = ('id',)


admin.site.register(MerchatTransactionsModel)
admin.site.site_header = "Let's Food Admin"
admin.site.site_title = "Let's Food Admin"
admin.site.index_title = "Let's Food Admin"
admin.site.register(Orders, OrderAdmin)
admin.site.register(MenuLunch, MenuLunchAdmin)
admin.site.register(MenuDinner, MenuDinnerAdmin)
