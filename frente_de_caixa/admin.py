from django.contrib import admin
from .models import Venda, ItemDeVenda


class VendaAdmin(admin.ModelAdmin):
    fields = ['cliente']
    list_display = ('id', 'cliente', 'itens_venda', 'valor_final')


class ItensDeVendaAdmin(admin.ModelAdmin):
    fields = ['venda', 'produto', 'servico', 'quantidade']
    list_display = ('id', 'venda', 'produto', 'quantidade', 'valor_total')


admin.site.register(Venda, VendaAdmin)
admin.site.register(ItemDeVenda, ItensDeVendaAdmin )
