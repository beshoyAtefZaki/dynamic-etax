"""einovice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from .api_views import InvoiceApi ,InvoiceListApi
from django.urls import path
from .views import (invoice_list,upload_from_vue,get_invoices_status,upload_vue ,
                    upload_page,create_inoice ,edit_invocie , post_update_status 
                     ,post_to_auth,export_to_excel,notify_user,cancel_invoice,get_document_printout)
urlpatterns = [
    path('invoice_list' ,invoice_list , name='invoice_list' ),
    path('create_inoice' ,create_inoice , name='create_inoice' ),
    path('edit_invocie/<id>' ,edit_invocie , name='edit_invocie' ),
    # path('upload' ,uplaod_sheet, name='upload'),
    path('post_update_status' ,post_update_status, name='post_update_status'),
    path('upload_from_vue' ,upload_from_vue, name='upload_from_vue'),
    #path('upload_page/<id>' ,upload_page, name='upload_page'),
    path('upload_vue/<id>' ,upload_vue, name='upload_vue'),
    path('post_to_auth/<id> ' ,post_to_auth, name='post_to_auth'),
    path('export_to_excel',export_to_excel,name='export_to_excel') ,
    path('invocie-list-api', InvoiceApi.as_view(), name='invocie-list-api'),
    path('invoice-list-vue', InvoiceListApi.as_view(), name='invoice-list'),
    path('get_invoices_status',get_invoices_status,name='get_invoices_status'),
    path('notify_user',notify_user,name='notify_user'),
    path('cancel_invoice',cancel_invoice,name='cancel_invoice'),
    path('get_document_printout/<uuid>',get_document_printout,name='get_document_printout')
]