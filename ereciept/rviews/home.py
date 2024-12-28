from django.shortcuts import render ,redirect
from ereciept import models as tables
from django.core.paginator import Page, Paginator

Receiept = tables.ereciept.Receiept
from ereciept.views import init_tax_sup_types , init_tax_types

def home(request) :
    
    receiepts = Receiept.objects.all().exclude(docstatus=-1)
    active_receiept = Receiept.objects.filter(docstatus=-1)
    if request.GET.get("search_fdate"):
        receiepts =receiepts.filter(created_at__gte=request.GET.get("search_fdate"))
    if request.GET.get("search_tdate"):
       receiepts=receiepts.filter(created_at__lte=request.GET.get("search_tdate"))
    if request.GET.get("search_tdate"):
       receiepts=receiepts.filter(created_at__lte=request.GET.get("search_tdate"))
    if request.GET.get("search_subid"):
       receiepts=receiepts.filter(submitionid=request.GET.get("search_subid"))
    if request.GET.get("search_uuid"):
       receiepts=receiepts.filter(t_uid = request.GET.get("search_uuid"))
    paginator = Paginator(receiepts  ,10)
    page_number = request.GET.get('page')
    receiepts_list = paginator.get_page(page_number)
    htmlpage = "pages/reciept_list.html"
    content = {
        "receiepts" : receiepts_list,
        "new_receiept" : active_receiept
    }
    return render(request ,htmlpage,content)


