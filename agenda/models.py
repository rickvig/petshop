from django.db import models
from datetime import datetime
from core.models import *


class Agenda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return self.cliente.__str__()

class OrdemServicoAbstrata(models.Model):
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


class OrdemServicoExterna(OrdemServicoAbstrata):
    animals = models.ManyToManyField(Animal)
