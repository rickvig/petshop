from django.contrib import admin
from .models import Agenda, OrdemServicoExterna, OrdemServicoInterna

class AgendaAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'ordens_servico']

class OrderServicoAdmin(admin.ModelAdmin):
    list_display = ['servico', 'data_horario_inicial', 'data_horario_final']

admin.site.register(Agenda, AgendaAdmin)
admin.site.register(OrdemServicoExterna, OrderServicoAdmin)
admin.site.register(OrdemServicoInterna, OrderServicoAdmin)