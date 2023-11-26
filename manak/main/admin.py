from django.contrib import admin
from .models import UIManager,MainTables,DataManager

# Register your models here.
class UIManagerAdmin(admin.ModelAdmin):
    list_display = ['modified_date','text_description','UI_position']
    search_fields = ['modified_date','text_description','UI_position']

class MainTablesAdmin(admin.ModelAdmin):
    fields = ['modified_date','carat_range','tabel_date','shape','text_description',]

class DataManagerAdmin(admin.ModelAdmin):
    pass


admin.site.register(UIManager, UIManagerAdmin)
admin.site.register(MainTables, MainTablesAdmin)
admin.site.register(DataManager, DataManagerAdmin)