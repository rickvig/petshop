from django.db import models
from core.models import Produto
from frente_de_caixa.models import Venda

class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data_entrada = models.DateField()
    data_saida = models.DateField(blank=True, null=True)
    data_validade = models.DateField()

    def __str__(self):
        return self.produto.__str__() + ' | ' 
        + str(self.quantidade) + self.produto.unidade_medida

class FluxoDeCaixa(models.Model):
    vendas = models.ManyToManyField(Venda)
    data_hora_abertura = models.DateTimeField()
    data_hora_fechamento = models.DateTimeField()
    valor_abertura = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)
    valor_fechamento = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)
    valor_final = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)

    