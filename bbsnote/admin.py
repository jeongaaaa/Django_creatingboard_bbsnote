from django.contrib import admin
from .models import *
#from .models import Board, Comment

# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    search_fields = ['subject', 'content']

admin.site.register(Board, BoardAdmin)
admin.site.register(Comment)