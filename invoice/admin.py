from django.contrib import admin

# Register your models here.
from .models import EInvoice , InvoiceLine,InoiveFile


admin.site.register(EInvoice)
admin.site.register( InvoiceLine)
admin.site.register(InoiveFile)