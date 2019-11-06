from django.db import models
from datetime import datetime
from polymorphic.models import PolymorphicModel
from core.models import Produto, Cliente, Fornecedor


class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data_entrada = models.DateField()
    data_saida = models.DateField(blank=True, null=True)
    data_validade = models.DateField()

    def __str__(self):
        return self.produto.__str__() + ' | '
        + str(self.quantidade) + self.produto.unidade_medida


class Movimentacao(PolymorphicModel):
    valor_final = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, default=0)
        
    def save(self, *args, **kwargs):
        self.calcula_valor_final()
        super().save(*args, **kwargs)


class Venda(Movimentacao):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def itens_venda(self):
        return list(self.itemdevenda_set.all())

    def calcula_valor_final(self):
        for item in list(self.itemdevenda_set.all()):
            self.valor_final += item.valor_total
    
    def __str__(self):
        return 'Venda: %i' % self.id
    

class ItemDeVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, blank=True, null=True)
    quantidade = models.DecimalField(max_digits=5, decimal_places=2)
    valor_total = models.DecimalField(max_digits=5, decimal_places=2)

    def calcula_valor_total(self):
        self.valor_total = self.quantidade * self.produto.valor_venda

    def save(self, *args, **kwargs):
        self.calcula_valor_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return "Qnt: %d. %s - %s" % (self.quantidade, self.produto.unidade_medida, self.produto.__str__())


class Compra(Movimentacao):
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)

    def itens_compra(self):
        return list(self.itemdecompra_set.all())

    def calcula_valor_final(self):
        for item in list(self.itemdecompra_set.all()):
            self.valor_final += item.valor_total

    def __str__(self):
        return 'Compra: %i' % self.id



class ItemDeCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, blank=True, null=True)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    def valor_unitario(self):
        return self.produto.valor_compra

    def calcula_valor_total(self):
        print('OPA: ', self.quantidade, self.produto.valor_compra)
        self.valor_total = self.quantidade * self.produto.valor_compra

    def save(self, *args, **kwargs):
        self.calcula_valor_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return "Qnt: %d. %s - %s" % (self.quantidade, self.produto.unidade_medida, self.produto.__str__())


class FluxoDeCaixa(models.Model):
    movimentacoes = models.ManyToManyField(Movimentacao)
    data_hora_abertura = models.DateTimeField()
    data_hora_fechamento = models.DateTimeField(null=True)
    valor_abertura = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    valor_fechamento = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    valor_final = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0)

    def atualiza_valor_fechamento(self):
        valor_aux = 0
        for movimentacao in self.movimentacoes.all():
            print('OPA', type(movimentacao))
            if type(movimentacao) == Venda:
                valor_aux += movimentacao.valor_final
            
            if type(movimentacao) == Compra:
                valor_aux -= movimentacao.valor_final

        self.valor_fechamento = valor_aux

    def fecha_caixa(self):
        self.valor_final = self.valor_abertura + self.valor_fechamento
        self.data_hora_fechamento = datetime.now()
