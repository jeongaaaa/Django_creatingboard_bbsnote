from django.contrib import admin
from .models import *
#from .models import Board, Comment

# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    search_fields = ['subject', 'content']

admin.site.register(Board, BoardAdmin)
#admin페이지에서 comment를 관리할 수 있도록 추가
admin.site.register(Comment)