from django.contrib import admin
from .models import Graph

class GraphAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'roomID')

# Register your models here.

admin.site.register(Graph, GraphAdmin)