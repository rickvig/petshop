from django.db import models
from core.models import Produto

# Create your models here.
class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data_entrada = models.DateField()
    data_saida = models.DateField(blank=True, null=True)
    data_validade = models.DateField()

    def __str__(self):
        return self.produto.__str__() + ' | ' 
        + str(self.quantidade) + self.produto.unidade_medida