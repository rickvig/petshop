from django.contrib import admin
from .models import Estoque, FluxoDeCaixa, Compra, ItemDeCompra, Venda, ItemDeVenda


class VendaAdmin(admin.ModelAdmin):
    fields = ['cliente']
    list_display = ('id', 'cliente', 'itens_venda', 'valor_final')


class ItensDeVendaAdmin(admin.ModelAdmin):
    fields = ['venda', 'produto', 'servico', 'quantidade']
    list_display = ('id', 'venda', 'produto', 'quantidade', 'valor_total')


class CompraAdmin(admin.ModelAdmin):
    fields = ['fornecedor']
    list_display = ('id', 'fornecedor', 'itens_compra', 'valor_final')


class ItensDeCompraAdmin(admin.ModelAdmin):
    fields = ['compra', 'produto', 'quantidade']
    list_display = ('id', 'compra', 'produto', 'valor_unitario', 'quantidade', 'valor_total')

admin.site.register(Estoque)
admin.site.register(FluxoDeCaixa)
admin.site.register(Venda, VendaAdmin)
admin.site.register(ItemDeVenda, ItensDeVendaAdmin )
admin.site.register(Compra, CompraAdmin)
admin.site.register(ItemDeCompra, ItensDeCompraAdmin)
