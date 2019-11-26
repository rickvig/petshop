from django.test import TestCase
from datetime import datetime, timedelta
from decimal import Decimal
from core.models import Produto, Cliente, Fornecedor
from .models import *


class TestMovimentacao(TestCase):

    cliente = Cliente()
    fornecedor = Fornecedor()

    def setUp(self):
        self.cliente = Cliente(nome="Henrique", renda=100.00, credito=100.00, status=True)
        self.cliente.save()

        self.fornecedor = Fornecedor(nome="Fornecedor Teste")
        self.fornecedor.save()

    def test_calcula_valor_total_do_item_venda(self):
        item_de_venda = ItemDeVenda()
        item_de_venda.produto = self.cria_produto(valor_venda=5.00, valor_compra=0.00)
        item_de_venda.quantidade = 15
        item_de_venda.calcula_valor_total()

        self.assertEqual(75, item_de_venda.valor_total)

    def test_calcula_valor_de_venda(self):
        venda_01 = Venda(cliente=self.cliente)
        venda_01.save()

        item_1 = ItemDeVenda()
        item_1.produto = self.cria_produto(5.00, 0.00)
        item_1.quantidade = 3
        item_1.calcula_valor_total()
        item_1.venda = venda_01
        item_1.save()

        item_2 = ItemDeVenda()
        item_2.produto = self.cria_produto(2.00, 0.00)
        item_2.quantidade = 2
        item_2.calcula_valor_total()
        item_2.venda = venda_01
        item_2.save()

        item_3 = ItemDeVenda()
        item_3.produto = self.cria_produto(1.50, 0.00)
        item_3.quantidade = 3.5
        item_3.calcula_valor_total()
        item_3.venda = venda_01
        item_3.save()

        venda_01.calcula_valor()
        self.assertEqual(24.25, venda_01.valor)

    def test_cria_fluxo_de_caixa_para_venda(self):
        fluxo_de_caixa = FluxoDeCaixa(data_hora_abertura=datetime.now())
        fluxo_de_caixa.valor_abertura = Decimal(1500.00)
        fluxo_de_caixa.save()

        fluxo_de_caixa.movimentacoes.add(self.cria_venda(75.00))
        fluxo_de_caixa.atualiza()
        self.assertEqual(75.00, fluxo_de_caixa.valor_em_fluxo)

        fluxo_de_caixa.movimentacoes.add(self.cria_venda(37.50))
        fluxo_de_caixa.atualiza()
        self.assertEqual(112.50, fluxo_de_caixa.valor_em_fluxo)

        fluxo_de_caixa.movimentacoes.add(self.cria_venda(15.00))
        fluxo_de_caixa.atualiza()
        self.assertEqual(127.50, fluxo_de_caixa.valor_em_fluxo)

        fluxo_de_caixa.movimentacoes.add(self.cria_venda(125.00))
        fluxo_de_caixa.atualiza()
        self.assertEqual(252.50, fluxo_de_caixa.valor_em_fluxo)

        fluxo_de_caixa.fecha_caixa()
        self.assertEqual(1752.50, fluxo_de_caixa.valor_final)
        self.assertEqual(datetime.now().date(),
                         fluxo_de_caixa.data_hora_fechamento.date())

    def test_cria_fluxo_de_caixa_para_compra(self):
        fluxo_de_caixa = FluxoDeCaixa(data_hora_abertura=datetime.now())
        fluxo_de_caixa.valor_abertura = Decimal(1500.00)
        fluxo_de_caixa.save()

        fluxo_de_caixa.movimentacoes.add(self.cria_compra(100.00))
        fluxo_de_caixa.atualiza()
        self.assertEqual(-100.00, fluxo_de_caixa.valor_em_fluxo)

        fluxo_de_caixa.movimentacoes.add(self.cria_compra(250.00))
        fluxo_de_caixa.atualiza()
        self.assertEqual(-350.00, fluxo_de_caixa.valor_em_fluxo)

        fluxo_de_caixa.movimentacoes.add(self.cria_compra(575.25))
        fluxo_de_caixa.atualiza()
        self.assertEqual(-925.25, fluxo_de_caixa.valor_em_fluxo)

        fluxo_de_caixa.fecha_caixa()
        self.assertEqual(574.75, fluxo_de_caixa.valor_final)
        self.assertEqual(datetime.now().date(),
                         fluxo_de_caixa.data_hora_fechamento.date())

    def test_cria_fluxo_de_caixa_para_os_interna(self):
        fluxo_de_caixa = FluxoDeCaixa(data_hora_abertura=datetime.now())
        fluxo_de_caixa.valor_abertura = Decimal(1500.00)
        fluxo_de_caixa.save()

        produto_shampo = self.cria_produto(15.00, 0.00)
        produto_condicionador = self.cria_produto(3.50, 0.00)

        estoque_shampo = Estoque()
        estoque_shampo.produto = produto_shampo
        estoque_shampo.quantidade = 20
        estoque_shampo.save()
        
        estoque_condicionador = Estoque()
        estoque_condicionador.produto = produto_condicionador
        estoque_condicionador.quantidade = 5
        estoque_condicionador.save()

        produtos = [ produto_shampo, produto_condicionador ]


        os_interna1 = self.cria_order_servico_interna(Decimal(100.00), produtos)

        fluxo_de_caixa.movimentacoes.add(os_interna1)
        fluxo_de_caixa.atualiza()
        self.assertEqual(Decimal(118.50), fluxo_de_caixa.valor_em_fluxo)

        os_interna2 = self.cria_order_servico_interna(Decimal(75.00), [])

        fluxo_de_caixa.movimentacoes.add(os_interna2)
        fluxo_de_caixa.atualiza()
        self.assertEqual(Decimal(193.50), fluxo_de_caixa.valor_em_fluxo)

        os = self.cria_order_servico_externa(Decimal(25.00))

        fluxo_de_caixa.movimentacoes.add(os)
        fluxo_de_caixa.atualiza()
        self.assertEqual(Decimal(218.50), fluxo_de_caixa.valor_em_fluxo)

        fluxo_de_caixa.fecha_caixa()

        estoque_shampo.movimentacoes.add(os_interna1)
        estoque_shampo.movimentacoes.add(os_interna2)
        estoque_shampo.atualiza()

        estoque_condicionador.movimentacoes.add(os_interna1)
        estoque_condicionador.movimentacoes.add(os_interna2)
        estoque_condicionador.atualiza()

        self.assertEqual(19, estoque_shampo.quantidade)
        self.assertEqual(4, estoque_condicionador.quantidade)

        self.assertEqual(1718.50, fluxo_de_caixa.valor_final)
        self.assertEqual(datetime.now().date(),
                         fluxo_de_caixa.data_hora_fechamento.date())

    def test_quantidade_em_estoque_para_compra_de_produto(self):
        produto = self.cria_produto(5.00, 1.50)

        estoque = Estoque(produto=produto, quantidade=50)
        estoque.save()

        compra = Compra(fornecedor=self.fornecedor)
        compra.save()

        item = ItemDeCompra(produto=produto, quantidade=50, compra=compra)
        item.save()

        compra.save()

        estoque.movimentacoes.add(compra)
        estoque.atualiza()

        self.assertEqual(100, estoque.quantidade)

    
    def test_quantidade_em_estoque_para_venda_de_produto(self):
        produto = self.cria_produto(5.00, 1.50)

        estoque = Estoque(produto=produto, quantidade=50)
        estoque.save()

        venda = Venda(cliente=self.cliente)
        venda.save()

        item = ItemDeVenda(produto=produto, quantidade=3, venda=venda)
        item.save()

        venda.save()

        estoque.movimentacoes.add(venda)
        estoque.atualiza()

        self.assertEqual(47, estoque.quantidade)


    def cria_produto(self, valor_venda, valor_compra):
        produto = Produto(descricao="Produto Teste",
                          valor_venda=valor_venda, valor_compra=valor_compra)
        produto.save()
        return produto

    def cria_venda(self, valor):
        venda = Venda(cliente=self.cliente)
        venda.save()

        item = ItemDeVenda(produto=self.cria_produto(
            valor, 0.00), quantidade=1, venda=venda)
        item.save()

        venda.save()
        return venda

    def cria_compra(self, valor):
        compra = Compra(fornecedor=self.fornecedor)
        compra.save()

        item = ItemDeCompra(produto=self.cria_produto(
            0.00, valor), quantidade=1, compra=compra)
        item.save()

        compra.save()
        return compra

    def cria_order_servico_interna(self, valor, produtos):
        agenda = Agenda(cliente=self.cliente)
        agenda.save()

        servico = Servico(descricao="Servico Teste", valor_venda=valor)
        servico.save()

        especie = Especie(nome="Gato")
        especie.save()

        raca = Raca(nome="Siamês", especie=especie)
        raca.save()

        animal = Animal(nome="Aimal Teste", dono=self.cliente, raca=raca)
        animal.save()

        os = OrdemServicoInterna(
            agenda=agenda,
            servico=servico,
            animal=animal,
            data_horario_inicial=datetime.now(),
            data_horario_final=datetime.now() + timedelta(hours=1))

        os.save()
        os.produtos.set(produtos)
        os.save()

        return os

    def cria_order_servico_externa(self, valor):
        agenda = Agenda(cliente=self.cliente)
        agenda.save()

        servico = Servico(descricao="Servico Teste", valor_venda=valor)
        servico.save()

        os = OrdemServicoExterna(
            agenda=agenda,
            servico=servico,
            data_horario_inicial=datetime.now(),
            data_horario_final=datetime.now() + timedelta(hours=1))

        os.save()
        return os
