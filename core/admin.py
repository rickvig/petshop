from django.contrib import admin
from .models import *

class ProdutoAdmin(admin.ModelAdmin):
    fields = ('descricao', 'valor_venda', 'valor_compra', 'codigo_barras', 'quantidade_estoque', 'unidade_medida', 'status')
    list_display = ('descricao', 'quantidade_estoque', 'unidade_medida', 'status')

admin.site.register(Cliente)
admin.site.register(Fornecedor)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Servico)