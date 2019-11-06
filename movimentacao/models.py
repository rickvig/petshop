from django.db import models
from datetime import datetime
from polymorphic.models import PolymorphicModel
from core.models import *


class Movimentacao(PolymorphicModel):
    valor = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        self.calcula_valor()
        super().save(*args, **kwargs)


class Venda(Movimentacao):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def itens_venda(self):
        return list(self.itemdevenda_set.all())

    def calcula_valor(self):
        for item in list(self.itemdevenda_set.all()):
            self.valor += item.valor_total

    def __str__(self):
        return 'Venda: %i' % self.id


class ItemDeVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, blank=True, null=True)
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

    def calcula_valor(self):
        for item in list(self.itemdecompra_set.all()):
            self.valor += item.valor_total

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
        self.valor_total = self.quantidade * self.produto.valor_compra

    def save(self, *args, **kwargs):
        self.calcula_valor_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return "Qnt: %d. %s - %s" % (self.quantidade, self.produto.unidade_medida, self.produto.__str__())


class Agenda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def ordens_servico(self):
        return list(self.ordemservicointerna_set.all()) + list(self.ordemservicoexterna_set.all())

    def __str__(self):
        return self.cliente.__str__()


class OrdemServicoAbstrata(Movimentacao):
    class Meta:
        abstract = True

    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    data_horario_inicial = models.DateTimeField()
    data_horario_final = models.DateTimeField()

    def __str__(self):
        return self.servico.__str__() + ' - ' + str(self.data_horario_inicial) + ' - ' + str(self.data_horario_final)


class OrdemServicoInterna(OrdemServicoAbstrata):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    checkin = models.DateTimeField(blank=True, null=True)
    checkout = models.DateTimeField(blank=True, null=True)
    produtos = models.ManyToManyField(Produto)

    def calcula_valor(self):
        self.valor = self.servico.valor_venda
        try:
            for produto in self.produtos.all():
                self.valor += produto.valor_venda
        except ValueError:
            print('ainda não tem  os produtos')


class OrdemServicoExterna(OrdemServicoAbstrata):
    animals = models.ManyToManyField(Animal)

    def calcula_valor(self):
        self.valor = self.servico.valor_venda


class FluxoDeCaixa(models.Model):
    movimentacoes = models.ManyToManyField(Movimentacao)
    data_hora_abertura = models.DateTimeField()
    data_hora_fechamento = models.DateTimeField(null=True)
    valor_abertura = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    valor_em_fluxo = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    valor_final = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0)

    def atualiza(self):
        valor_aux = 0
        for movimentacao in self.movimentacoes.all():
            if type(movimentacao) == Venda:
                valor_aux += movimentacao.valor

            if type(movimentacao) == Compra:
                valor_aux -= movimentacao.valor
            
            if type(movimentacao) == OrdemServicoInterna:
                valor_aux += movimentacao.valor
            
            if type(movimentacao) == OrdemServicoExterna:
                valor_aux += movimentacao.valor

        self.valor_em_fluxo = valor_aux

    def fecha_caixa(self):
        self.valor_final = self.valor_abertura + self.valor_em_fluxo
        self.data_hora_fechamento = datetime.now()



class Estoque(models.Model):
    movimentacoes = models.ManyToManyField(Movimentacao)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)
    data_validade = models.DateField(blank=True, null=True)

    def atualiza(self):
        calculo = 0
        for movimentacao in self.movimentacoes.all():
            if type(movimentacao) == Venda:
                for item in movimentacao.itemdevenda_set.all():
                    if item.produto == self.produto:
                        calculo -= item.quantidade

            if type(movimentacao) == Compra:
                for item in movimentacao.itemdecompra_set.all():
                    if item.produto == self.produto:
                        calculo += item.quantidade
            
            if type(movimentacao) == OrdemServicoInterna:
                calculo += movimentacao.valor
            
        self.quantidade += calculo

    def __str__(self):
        return self.produto.__str__() + ' | '
        + str(self.quantidade) + self.produto.unidade_medida