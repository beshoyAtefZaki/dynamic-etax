from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# required import.
from django.views import generic
from .models import EInvoice
from rest_framework import viewsets
from rest_framework.response import Response

from .serializer import InvoiceLineSerializer  ,InvoiceSerializers


from rest_framework import pagination ,generics

class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10
    page_query_param = 'p'
    def get_paginated_response(self, data):
        response = Response(data)
        response['count'] = self.page.paginator.count
        response['next'] = self.get_next_link()
        response['previous'] = self.get_previous_link()
        return response
#class InvoiceList(generic.ListView):


class InvoiceApi(generics.ListAPIView):
    queryset = EInvoice.objects.all().order_by('-id')
    serializer_class = InvoiceSerializers
    agination_class = CustomPagination
   
class InvoiceListApi(generic.ListView):
    model = EInvoice
    agination_class = CustomPagination
    template_name = 'invoice_vue.html'
    def get_queryset(self):
        return EInvoice.objects.all().order_by('-id')
