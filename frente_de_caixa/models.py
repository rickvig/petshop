from django.db import models
from datetime import datetime
from core.models import *


class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    valor_final = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)

    def itens_venda(self):
        itens_str = ''
        for item in list(self.itemdevenda_set.all()):
            itens_str += item.__str__() + '\n'

        print(itens_str)
        return itens_str
    
    def save(self, *args, **kwargs):
        self.valor_final = 0
        super().save(*args, **kwargs)

    def calcula_valor_final(self):
        for item in list(self.itemdevenda_set.all()):
            self.valor_final += item.valor_total


    def __str__(self):
        return 'Venda: %i' % self.id


class ItemDeVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, blank=True, null=True)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, blank=True, null=True)
    quantidade = models.DecimalField(max_digits=5, decimal_places=2)
    valor_total = models.DecimalField(max_digits=5, decimal_places=2)

    def calcula_valor_total(self):
        self.valor_total = self.quantidade * self.produto.valor_venda

    def save(self, *args, **kwargs):
        self.calcula_valor_total()
        super().save(*args, **kwargs)
        
        self.venda.save()

    def __str__(self):
        return "Qnt: %d. %s - %s" % (self.quantidade, self.produto.unidade_medida, self.produto.__str__())
