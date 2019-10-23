from django.contrib import admin
from .models import Venda, ItensDeVenda


class VendaAdmin(admin.ModelAdmin):
    fields = ['cliente']
    list_display = ('cliente', 'itens_venda', 'valor_final')


class ItensDeVendaAdmin(admin.ModelAdmin):
    fields = ['venda', 'produto', 'servico', 'quantidade']
    list_display = ('venda', 'produto', 'quantidade', 'valor_total')


admin.site.register(Venda, VendaAdmin)
admin.site.register(ItensDeVenda, ItensDeVendaAdmin )
