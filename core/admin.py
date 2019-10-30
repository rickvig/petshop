from django.contrib import admin
from .models import *

class ProdutoAdmin(admin.ModelAdmin):
    fields = ('descricao', 'valor_venda', 'valor_compra', 'codigo_barras', 'unidade_medida', 'status')
    list_display = ('descricao', 'valor_venda', 'unidade_medida', 'status')

class AnimalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'raca', 'sexo', 'cor', 'idade', 'dono')

admin.site.register(Cliente)
admin.site.register(Fornecedor)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Servico)
admin.site.register(Estado)
admin.site.register(Cidade)
admin.site.register(Endereco)
admin.site.register(Telefone)
admin.site.register(Especie)
admin.site.register(Raca)
admin.site.register(Animal, AnimalAdmin)