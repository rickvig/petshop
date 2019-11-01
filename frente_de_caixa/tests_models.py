from django.test import TestCase

from .models import ItemDeVenda, Venda
from core.models import Produto, Cliente


class TestModelFrenteCaixa(TestCase):

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

