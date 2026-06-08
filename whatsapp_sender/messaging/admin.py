from django.contrib import admin
from .models import UploadedFile
from .excel_import import import_excel


# Register your models here.
@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        if not change:
            import_excel(obj.file.path)