from django.test import TestCase
from datetime import datetime
from decimal import Decimal
from .models import FluxoDeCaixa
from core.models import Produto, Cliente
from frente_de_caixa.models import ItemDeVenda, Venda

class TestModelFinanceiroEstoque(TestCase):
    
    def test_cria_processo_do_fluxo_de_caixa(self):
        
        fluxo_de_caixa = FluxoDeCaixa(data_hora_abertura=datetime.now())
        fluxo_de_caixa.valor_abertura = Decimal(1500.00)
        fluxo_de_caixa.save()
        
        fluxo_de_caixa.vendas.add(self.cria_venda(75.00))
        fluxo_de_caixa.atualiza_valor_fechamento()
        self.assertEqual(75.00, fluxo_de_caixa.valor_fechamento)

        fluxo_de_caixa.vendas.add(self.cria_venda(37.50))
        fluxo_de_caixa.atualiza_valor_fechamento()
        self.assertEqual(112.50, fluxo_de_caixa.valor_fechamento)

        fluxo_de_caixa.vendas.add(self.cria_venda(15.00))
        fluxo_de_caixa.atualiza_valor_fechamento()
        self.assertEqual(127.50, fluxo_de_caixa.valor_fechamento)

        fluxo_de_caixa.vendas.add(self.cria_venda(125.00))
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