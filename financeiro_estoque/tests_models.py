from django.test import TestCase
from datetime import datetime
from decimal import Decimal
from .models import FluxoDeCaixa, Compra, ItemDeCompra, ItemDeVenda, Venda
from core.models import Produto, Cliente, Fornecedor

class TestModelFinanceiroEstoque(TestCase):

    def test_calcula_item_venda_valor_total(self):
        item_de_venda = ItemDeVenda()
        item_de_venda.produto = Produto(descricao="Bolinha", valor_venda=5.00)
        item_de_venda.quantidade = 15
        item_de_venda.calcula_valor_total()

        self.assertEqual(75, item_de_venda.valor_total)

    def test_calcula_venda_valor_final(self):

        cliente = Cliente(nome="Henrique", renda=100.00, credito=100.00, status=True)
        cliente.save()

        venda_01 = Venda(cliente=cliente)
        venda_01.save()

        item_1 = ItemDeVenda()
        produto_1 = Produto(descricao="Bolinha", valor_venda=5.00)
        produto_1.save()
        item_1.produto = produto_1
        item_1.quantidade = 3
        item_1.calcula_valor_total()
        item_1.venda = venda_01
        item_1.save()

        item_2 = ItemDeVenda()
        produto_2 = Produto(descricao="Osso", valor_venda=2.00)
        produto_2.save()
        item_2.produto = produto_2
        item_2.quantidade = 2
        item_2.calcula_valor_total()
        item_2.venda = venda_01
        item_2.save()

        item_3 = ItemDeVenda()
        produto_3 = Produto(descricao="Ração Barata", valor_venda=1.50)
        produto_3.save()
        item_3.produto = produto_3 
        item_3.quantidade = 3.5
        item_3.calcula_valor_total()
        item_3.venda = venda_01
        item_3.save()

        venda_01.calcula_valor_final()

        self.assertEqual(24.25, venda_01.valor_final)
    
    def test_cria_processo_do_fluxo_de_caixa_venda(self):
        
        fluxo_de_caixa = FluxoDeCaixa(data_hora_abertura=datetime.now())
        fluxo_de_caixa.valor_abertura = Decimal(1500.00)
        fluxo_de_caixa.save()
        
        fluxo_de_caixa.movimentacoes.add(self.cria_venda(75.00))
        fluxo_de_caixa.atualiza_valor_fechamento()
        self.assertEqual(75.00, fluxo_de_caixa.valor_fechamento)

        fluxo_de_caixa.movimentacoes.add(self.cria_venda(37.50))
        fluxo_de_caixa.atualiza_valor_fechamento()
        self.assertEqual(112.50, fluxo_de_caixa.valor_fechamento)

        fluxo_de_caixa.movimentacoes.add(self.cria_venda(15.00))
        fluxo_de_caixa.atualiza_valor_fechamento()
        self.assertEqual(127.50, fluxo_de_caixa.valor_fechamento)

        fluxo_de_caixa.movimentacoes.add(self.cria_venda(125.00))
        fluxo_de_caixa.atualiza_valor_fechamento()
        self.assertEqual(252.50, fluxo_de_caixa.valor_fechamento)

        fluxo_de_caixa.fecha_caixa()

        self.assertEqual(252.50, fluxo_de_caixa.valor_fechamento)
        self.assertEqual(1752.50, fluxo_de_caixa.valor_final)
        self.assertEqual(datetime.now().date(), 
                        fluxo_de_caixa.data_hora_fechamento.date())


    def cria_venda(self, valor):
        cliente = Cliente(nome="Henrique", renda=100.00, credito=100.00, status=True)
        cliente.save()

        venda = Venda(cliente=cliente)
        venda.save()

        produto = Produto(descricao="Bolinha", valor_venda=valor)
        produto.save()

        item = ItemDeVenda()
        item.produto = produto
        item.quantidade = 1
        item.venda = venda
        item.save()
        
        venda.save()

        return venda

    
    def test_cria_processo_do_fluxo_de_caixa_compra(self):

        fluxo_de_caixa = FluxoDeCaixa(data_hora_abertura=datetime.now())
        fluxo_de_caixa.valor_abertura = Decimal(1500.00)
        fluxo_de_caixa.save()

        fluxo_de_caixa.movimentacoes.add(self.cria_compra(100.00))
        fluxo_de_caixa.atualiza_valor_fechamento()
        self.assertEqual(-100.00, fluxo_de_caixa.valor_fechamento)
        
        fluxo_de_caixa.movimentacoes.add(self.cria_compra(250.00))
        fluxo_de_caixa.atualiza_valor_fechamento()
        self.assertEqual(-350.00, fluxo_de_caixa.valor_fechamento)
        
        fluxo_de_caixa.movimentacoes.add(self.cria_compra(575.25))
        fluxo_de_caixa.atualiza_valor_fechamento()
        self.assertEqual(-925.25, fluxo_de_caixa.valor_fechamento)

        fluxo_de_caixa.fecha_caixa()

        self.assertEqual(-925.25, fluxo_de_caixa.valor_fechamento)
        self.assertEqual(574.75, fluxo_de_caixa.valor_final)
        self.assertEqual(datetime.now().date(), 
                        fluxo_de_caixa.data_hora_fechamento.date())

    def cria_compra(self, valor):
        fornecedor = Fornecedor(nome="Purina")
        fornecedor.save()

        compra = Compra(fornecedor=fornecedor)
        compra.save()

        produto = Produto(descricao="Bolinha", valor_compra=valor)
        produto.save()

        item = ItemDeCompra(produto=produto, quantidade=1, compra=compra)
        item.save()
        
        compra.save()

        return compra