from django.test import TestCase

from .models import ItensDeVenda, Venda
from core.models import Produto

class TestModelFrenteCaixa(TestCase):

    def test_calcula_item_venda_valor_total(self):
        item_de_venda = ItensDeVenda()
        item_de_venda.produto = Produto(descricao="Bolinha", valor_venda=5.00)
        item_de_venda.quantidade = 15
        item_de_venda.calcula_valor_total()

        self.assertEqual(item_de_venda.valor_total, 75)