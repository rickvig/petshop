from django.contrib import admin
from .models import *


class VendaAdmin(admin.ModelAdmin):
    fields = ['cliente']
    list_display = ('id', 'cliente', 'itens_venda', 'valor')


class ItensDeVendaAdmin(admin.ModelAdmin):
    fields = ['venda', 'produto', 'servico', 'quantidade']
    list_display = ('id', 'venda', 'produto', 'quantidade', 'valor_total')


class CompraAdmin(admin.ModelAdmin):
    fields = ['fornecedor']
    list_display = ('id', 'fornecedor', 'itens_compra', 'valor')


class ItensDeCompraAdmin(admin.ModelAdmin):
    fields = ['compra', 'produto', 'quantidade']
    list_display = ('id', 'compra', 'produto',
                    'valor_unitario', 'quantidade', 'valor_total')


class AgendaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'ordens_servico']


class OrderServicoAdmin(admin.ModelAdmin):
    list_display = ['servico', 'data_horario_inicial', 'data_horario_final']


admin.site.register(Estoque)
admin.site.register(FluxoDeCaixa)
admin.site.register(Venda, VendaAdmin)
admin.site.register(ItemDeVenda, ItensDeVendaAdmin)
admin.site.register(Compra, CompraAdmin)
admin.site.register(ItemDeCompra, ItensDeCompraAdmin)
admin.site.register(Agenda, AgendaAdmin)
admin.site.register(OrdemServicoExterna, OrderServicoAdmin)
admin.site.register(OrdemServicoInterna, OrderServicoAdmin)
