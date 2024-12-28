from distutils.command.upload import upload
from email import message
import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import pandas as pd
# Create your views here.
from django.core.paginator import Page, Paginator
from .models import EInvoice ,InoiveFile
from django.http import JsonResponse
from home.models import Receiver ,AccountType
from payer.models import PayerAccount
from tax.models import TaXCategory ,taxableItems ,TaxTotals
from http.client import HTTPSConnection
from base64 import b64encode, encode
import ssl
import subprocess
from django.db.models import Q
from .utils import queryset_to_workbook
from reports.views import get_token
from background_task import background
from django.views.decorators.csrf import csrf_exempt
import requests 
import threading
from .column import create_request
from payer.utils import get_payer_account
# from .models import EInvoice
# import commands


Acocunt = get_payer_account() 
PAYER_ACCOUNT = Acocunt.get("Account")
login_url     =  Acocunt.get("login_url")#'id.eta.gov.eg' if PAYER_ACCOUNT.environment == "Production" else 'id.preprod.eta.gov.eg'
api_url       = Acocunt.get("api_url")       #'api.invoicing.eta.gov.eg' if PAYER_ACCOUNT.environment == "Production" else 'api.preprod.invoicing.eta.gov.eg'


def invoice_list(request):
    
    invociesList =    EInvoice.objects.all().order_by('-id')
    fill_uploauded = InoiveFile.objects.all().order_by('-id')
    # get_invoices_status()
    if request.GET.get("uplaoder_id") :
        invociesList =    EInvoice.objects.filter(uploader_id =request.GET.get("uplaoder_id") ).order_by('-id')
    if request.GET.get("search"):
        invociesList = invociesList.filter( Q(internalId__icontains=request.GET.get("search")  ) |Q(receiver_name__icontains=request.GET.get("search")))
    if request.GET.get("from_date"):
        invociesList=invociesList.filter(created_date__gte=request.GET.get("from_date"))
    if request.GET.get("to_date"):
        invociesList=invociesList.filter(created_date__lte=request.GET.get("to_date"))
    if request.GET.get("customer"):
        invociesList = invociesList.filter( Q(receiver_name__icontains=request.GET.get("customer"))| Q(receiver_id__icontains=request.GET.get("customer")  ) )
    paginator = Paginator(invociesList , 20)
    page_number = request.GET.get('page')
    invocies = paginator.get_page(page_number)
    page = 'invoice_list.html'
    fl_select = [{"id" :i.id , "value" : i.status } for i in fill_uploauded ] 
    content = {
        "invoices" : invocies , 
        "fl_select" : fl_select ,
        "uploader_id" : InoiveFile.objects.filter(id = request.GET.get("uplaoder_id")).first() if request.GET.get("uplaoder_id") else  False,
        "serach_value" : request.GET.get("search") if request.GET.get("search") else "",
        "from_date" : request.GET.get("from_date") if request.GET.get("from_date") else "" ,
        "to_date" : request.GET.get("to_date") if request.GET.get("to_date") else "",
        "customer": request.GET.get("customer") if request.GET.get("customer") else ""
    }
    return render(request ,page , content ) 



def export_to_excel(request):
    invociesList = EInvoice.objects.all().order_by('-id')
    if  request.POST.get("uplaoder_id") :
         fill_uploauded = InoiveFile.objects.filter(status =request.POST.get("uplaoder_id")  ).last()
    if request.POST.get("search"):
        invociesList = invociesList.filter(
            Q(internalId__icontains=request.POST.get("search")) | Q(receiver_name__icontains=request.POST.get("search")))
    if request.POST.get("from_date"):
        print("from date")
        invociesList = invociesList.filter(created_date__gte=request.POST.get("from_date"))
    if request.POST.get("to_date"):
        invociesList = invociesList.filter(created_date__lte=request.POST.get("to_date"))
    if request.POST.get("customer"):
        invociesList = invociesList.filter( Q(receiver_name__icontains=request.POST.get("customer"))| Q(receiver_id__icontains=request.POST.get("customer")  ) )
    if request.POST.get("uplaoder_id"):
        invociesList = EInvoice.objects.filter(uploader_id=fill_uploauded.id)
    
    columns = [
        "internalId",
        "documentType",
        "documentTypeVersion",
        "dateTimeIssued",
        "receiver_type",
        "receiver_id",
        "receiver_name",
        "receiver_address_branchId",
        "receiver_address_country",
        "receiver_address_governate",
        "receiver_address_regionCity",
        "receiver_address_street",
        "receiver_address_buildingNumber",
        "netAmount",
        "taxTotals",
        "extraDiscountAmount",
        "totalItemsDiscountAmount",
        "totalAmount",
        "totalSalesAmount",
        "created_date",
        "submissionId"
    ]
    url = queryset_to_workbook(invociesList,columns)
    return JsonResponse({"url":url})

def create_inoice(request):
    page = 'invoice_create.html'
    types = [{'v' :i[0] , 'n' :i[1] }
                for i in AccountType ]
    receiver = Receiver.objects.all()
    issuer = PayerAccount.objects.all()
    receivers = [{"id" : i.id , "name" : i.receiver_name  } for i in receiver ]
    issuers = [{"id" : i.id , "name" : i.issuer_name  } for i in issuer ]
    content = {
        "types": types ,
        "receivers" :receivers,
        "issuers":issuers

    }
    if request.method == "POST":
        print(request.POST.get('issuer'))
        a = EInvoice(
            payer_account =  PayerAccount.objects.filter(id = request.POST.get('issuer')).first() , 
            receiver_account =Receiver.objects.filter(id = request.POST.get('receiver')).first() if request.POST.get('receiver') else None
        )
        receiver_account =Receiver.objects.filter(id = request.POST.get('receiver')).first()
       
        if receiver_account :
            a.receiver_type = receiver_account.receiver_type
            a.receiver_id= receiver_account.receiver_id
            a.receiver_name= receiver_account.receiver_name
            a.receiver_address_branchId = receiver_account.receiver_address_branchId
            a.receiver_address_country= receiver_account.receiver_address_country
            a.receiver_address_governate = receiver_account.receiver_address_governate
            a.receiver_address_regionCity= receiver_account.receiver_address_regionCity
            a.receiver_address_street = receiver_account.receiver_address_street
            a.receiver_address_buildingNumber = receiver_account.receiver_address_buildingNumber

        
        a.save()
       
        return redirect ('edit_invocie' , a.id)

    return render(request , page ,content)

def edit_invocie(request, id):
    page = 'invoice_create.html'
    types = [{'v' :i[0] , 'n' :i[1] }
                for i in AccountType ]
    receiver = Receiver.objects.all()
    issuer = PayerAccount.objects.all()
    receivers = [{"id" : i.id , "name" : i.receiver_name  } for i in receiver ]
    issuers = [{"id" : i.id , "name" : i.issuer_name  } for i in issuer ]
    invocie = EInvoice.objects.get(id =id)
    taxes  = invocie.taxTotals.all()

    print("taxes " , taxes)
    items = invocie.invoiceLines.all()
    stat = None
    if invocie.message_Serv :
        stat_message =invocie.message_Serv

        stat_v = stat_message[2:-1]
        stat = stat_v.replace('null' , '""')
    content = {
        "types": types ,
        "receivers" :receivers,
        "issuers":issuers ,
        "invoice" : invocie ,
        "stat" :stat,
        "taxes":taxes,
        "items":items

    }
    return render(request , page ,content)


def upload_vue(request ,id) :
    #step 2 in upload file to tax auth 
    """
    params id 
    invoice file id 
    we got the id after upload the sheet 
    
    """
    a = InoiveFile.objects.filter(id=id).first()
    try:
        success =create_request(a.id , a.sheet.path)
        print(success.get("message"))
        return JsonResponse({"success" : success.get("message")})
    except Exception as ex:
        print(ex)
        return JsonResponse ({"status":"error 2"  , 'message': str(ex)  })

#remove this 
def upload_page(request, id):
    
    page = "upload_page.html"
    a = InoiveFile.objects.filter(id=id).first()
    try:
        success =create_request(a.id , a.sheet.path)
        if success.get('error') :
            return render (request , "error.html" , {'message': success.get('error') })
    except Exception as ex:
        return render (request , "error.html" , {'message': str(ex) })

    
    return render(request , page)

@csrf_exempt
def post_update_status(request):
    if request.method== 'POST' :
        invocie_id        = request.POST.get("id")  
        message_Serv      = request.POST.get("message_Serv")  
        submissionId      = request.POST.get("submissionId") 
        uuid              = request.POST.get("uuid")
        obj               = EInvoice.objects.filter(id= invocie_id).first()  
        obj.submissionId  = submissionId if submissionId else  " "
        obj.uuid          = uuid  if uuid else  " "
        obj.message_Serv  = f" '{submissionId}'  " if submissionId else message_Serv
        obj.status        = "Submitted" if  submissionId else "Not Send"
        obj.save()
        print(f"obj Save {obj.id}")
        return JsonResponse({"message": "done"})
    else :
        return JsonResponse({"messgae" :"Erro Method Get"})
# def uplaod_sheet(request):
#     fl_select = {}
#     if request.method== 'POST' :
      
#         a = InoiveFile(
#             status = request.POST.get('sheettitle') ,
#             sheet =request.FILES['myfile'] )
#         a.save()
#         return redirect('upload_page' ,id =a.id)
        
    
        
#     invociesList =    EInvoice.objects.all().order_by('-id')
#     fill_uploauded = InoiveFile.objects.all().order_by('-id')
#     paginator = Paginator(invociesList , 20)
#     # page_number = request.GET.get('page')
#     invocies = paginator.get_page(1)
#     page = 'invoice_list.html'
    
#     content = {
#         "invoices" : invocies , 
#         "fl_select" : fl_select
#     }
#     return render(request ,page , content ) 


def upload_from_vue(request):
    
    fl_select = {}
    if request.method== 'POST' :
         
        a = InoiveFile(sheet =request.FILES['file'] )
        a.status = str(request.POST.get("title") or  "EX ")
        a.save()
        return JsonResponse({"messgae" : "upload" , "id" :a.id})
       
            
    invociesList =    EInvoice.objects.all().order_by('-id')
    paginator = Paginator(invociesList , 20)
    invocies = paginator.get_page(1)
    page = 'invoice_vue.html'
    
    content = {
        "invoices" : invocies , 
        "fl_select" : fl_select
    }
    return render(request ,page , content ) 

   


#add thread to sup proccess to complete

def add_tread_post_to_auth( id , *args , **kwargs ):
    
    invoice  = EInvoice.objects.filter(id=id).first()
    if not invoice :
        return JsonResponse({'error' : "Invocie Id Error "})
    form = { "documents":[{
        "issuer":{ 
									 "name"   : invoice.issuer_name ,
									 "id"     : invoice.issuer_id or "",
									 "type"   : invoice.issuer_type  ,
									 "address": {
									 			   "branchID"      :invoice.issuer_address_branchId or ''  ,
                                                    "country"    :invoice.issuer_address_country or '' ,
							 			           "governate"     :invoice.issuer_address_governate or ''  ,
                                                   "regionCity" : invoice.issuer_address_regionCity or '' ,
							 			           "street"        :invoice.issuer_address_street     ,
								  				   "buildingNumber":str(invoice.issuer_address_buildingNumber or '')
								  				
		
												} 
                } ,
         "receiver":{ 
									 "name"   : invoice.receiver_name ,
									 "id"     : invoice.receiver_id or "",
									 "type"   : invoice.receiver_type  ,
									 "address": {
									 			   "branchID"      :invoice.receiver_address_branchId or ''  ,
                                                    "country"    :invoice.receiver_address_country or '' ,
							 			           "governate"     :invoice.receiver_address_governate or ''  ,
                                                   "regionCity" : invoice.receiver_address_regionCity or '' ,
							 			           "street"        :invoice.receiver_address_street     ,
								  				   "buildingNumber":str(invoice.receiver_address_buildingNumber or '')
								  				
		
												} 
                } ,
        #main info Section 
        "documentType"             :invoice.documentType,
        "documentTypeVersion"      :invoice.documentTypeVersion , 
        # 2021-05-17 12:21:11
        "dateTimeIssued"            :invoice.datetimestr ,
        "taxpayerActivityCode"     : str(invoice.taxpayerActivityCode ) ,
        "internalID"               : str(invoice.internalId or ''),
        "purchaseOrderReference"   : "",#str(self.purchase_order_reference or ''),
        "purchaseOrderDescription" : "" ,
        "salesOrderReference"      : "" ,
        "salesOrderDescription"    : "" ,
        "proformaInvoiceNumber"    : "" ,
        

        #Item section 
        "invoiceLines" :[ {
		              'description'     :item.description,
		              'itemType'        :item.itemType,
		              'itemCode'        :item.itemCode,
		              'unitType'        :item.unitType,
		              'quantity'        :int(item.quantity),
		              'internalCode'    :item.itemCode,
		              'salesTotal'      :round(float(item.salesTotal or 0 ) ,5),
		              'total'           :round( float(item.total or 0) , 5) ,
		              'valueDifference' :float(item.valueDifference or 0) , 
		              'totalTaxableFees':0 ,#float(item.total_taxable_fees or 0),
		              'netTotal'        :round(float(item.netTotal or 0) , 5 )  ,
		              'itemsDiscount'   : 0, #round((item.item_discount * item.quantity) , 5),
		              'unitValue'       :   {
		                                    'currencySold'        :item.unitValue_currencySold,
		                                    'amountEGP'           :round(float(item.unitValue_amountEGP) , 5),
		                                    'amountSold'          :float(item.unitValue_amountSold or 0),
		                                    'currencyExchangeRate':float(item.unitValue_currencyExchangeRate or 0 ),
		                                    },
		              'discount'        :  {
		                                   'rate':0,
		                                    'amount':round((float(item.discount_amount  or 0) *float(item.quantity) ), 5)
		                                    },

                        "taxableItems" :[ {"taxType":tax_i.taxType ,
                                           "amount": round(float(tax_i.amount or 0 ) , 5) , 
                                            "subType" : tax_i.subType ,
                                            "rate" :round( float ( tax_i.rate or 0) , 5 )} 
                                             for tax_i in  item.taxableItems.all()]
                     
		             
		   	 }


         for item in  invoice.invoiceLines.all()] , 

        #total Section 
        "totalDiscountAmount"      :float(invoice.totalDiscountAmount or 0),
        "totalSalesAmount"         :float(invoice.totalSalesAmount or 0) ,
        "netAmount"                :float(invoice.netAmount or 0),
        "taxTotals"                : [
            {
                "taxType" : tax_e.taxType ,
                "amount" : round( float (tax_e.amount or 0))
            }
        for tax_e in  
        invoice.taxTotals.all()],#invoice.taxTotals.all(),
        "totalAmount"              :float(invoice.totalAmount or 0)   ,
        "extraDiscountAmount"      :0,
        "totalItemsDiscountAmount" :0 ,


		


    }]
    }
    token = get_token()
    headers = {
				"Authorization"   : 'Bearer %s'%token,
				"Accept"          : "application/json" ,
				"Accept-Language" : "ar" ,
				'Content-Type'    :'application/json' 
				}
    if invoice.documentTypeVersion == "0.9"  :
        print(invoice.documentTypeVersion )
        c = HTTPSConnection('api.preprod.invoicing.eta.gov.eg' ,context=ssl._create_unverified_context())
        c.request('POST', '/api/v1.0/documentsubmissions' ,headers=headers , body=json.dumps(form) )
        res = c.getresponse()
        data = res.read()
        invoice.message_Serv = str(data)
        return JsonResponse({'message' : str(data)})
    if invoice.documentTypeVersion == "1.0"  :
        try :
          os.remove('C:/j/sFile.txt')
        except:
            pass
        jsonfile = "C:/j/sFile.txt"
        with open(jsonfile, 'a', encoding='utf-8') as outfile:
            json.dump(input_json, outfile )

        cmd = 'C:/j/EInvoicingSigner.exe'
        result = subprocess.Popen([cmd ,' '], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        a,b = result.communicate()
        main_data={}
       
        if a :
            try :
                h = json.loads(a)
                if h.get('submissionId') :
                    accepted_document = {"document_id" : internal_id  , "submissionId" :h.get('submissionId') }
                    # if h.get('submissionId') : 
                    #     main_data['submissionId'] =  h.get('submissionId')
                    # self.request.sendall(json.dumps(accepted_document).encode('utf-8'))
                    return JsonResponse({'message' : str(accepted_document)})

                else :
                    try :
                        rejected = h.get('rejectedDocuments')[0].get('error').get('details')[0]
                        main_data['error_details'] =rejected or b
                        return JsonResponse({'message' : str(main_data)})
                    
                    
                    except:
                        main_data['error_details'] =b
                        return JsonResponse({'message' : str(main_data)})
            except :
                 return JsonResponse({'message' : "Erro"})

                  
        else :
            main_data['error_details'] =str(b)
            return JsonResponse({'message' : str(main_data)})


def post_to_auth(request , id ):
    import threading
    #add_tread_post_to_auth(id)
    processThread = threading.Thread(target=add_tread_post_to_auth, args=(id,))  # <- note extra ','
    processThread.start()
    return JsonResponse({'message' : 'process'})
def get_invoices_status():
   
    invoices  =  EInvoice.objects.filter(uuid__isnull=False,status__in=['Submitted',"Valid","Valid To Cancel"])
    
    token = get_token()
    #c = HTTPSConnection(url ,context=ssl._create_unverified_context())
    headers = {
				"Authorization"   : 'Bearer %s'%token,
				"Accept"          : "application/json" ,
				"Accept-Language" : "ar" ,
				'Content-Type'    :'application/json' 
		}
    for inv in invoices:
        #print("internal id",inv.internalId,inv.status)
        try:
            method_url = f"/api/v1/documents/{inv.uuid}/raw"
            c = HTTPSConnection(api_url ,context=ssl._create_unverified_context())
            c.request('GET', method_url ,headers=headers)
            res = c.getresponse()
            data = res.read()
            data = json.loads(data)
            status = data.get("status")
            if status == "Valid" and inv.status == "Valid To Cancel":
                continue
            inv.status = status
            inv.save()
        except Exception as ex:
            print(str(ex)) 
    
    return JsonResponse({"status":"s"})




def cancel_invoice(request):
    
    id      = request.POST.get("id")
    reason  = request.POST.get("reason")
    inv     = EInvoice.objects.filter(pk=id).first()
    token   = get_token()
    headers = {
				"Authorization"   : 'Bearer %s'%token,
				"Accept"          : "application/json" ,
				"Accept-Language" : "ar" ,
				'Content-Type'    :'application/json' 
		}
    body = {
        "status":"cancelled",
        "reason":"reason"
    }

    method_url = f"/api/v1.0/documents/state/{inv.uuid}/state"
    c = HTTPSConnection(api_url ,context=ssl._create_unverified_context())
    c.request('PUT', method_url ,headers=headers,body=json.dumps(body))
    res =  c.getresponse()
    data = res.read().decode('UTF-8')
    print("data =======> ",data)
    if data == "true":
        inv.status= "Valid To Cancel"
        inv.save()
    return redirect('invoice_list')
        
    return JsonResponse({"response":data})



@background(schedule=500)
def call_get_inv_status():
    get_invoices_status()


def notify_user(request):
    #get_invoices_status()
    call_get_inv_status()
    return JsonResponse({"status":"success"})



       
def get_document_printout(request,uuid):
    method_url ="https://"+api_url+ f"/api/v1.0/documents/{uuid}/pdf"
    token   = get_token()
    headers = {
				"Authorization"   : 'Bearer %s'%token,
				"Accept"          : "*/*" 
		}
    r= requests.get(method_url,headers=headers)
    if r.status_code==200:
        filename=f"{uuid}.pdf"
        with open(f'pdfinvoicesfolder/{filename}', 'wb') as f:
            f.write(r.content)
        return HttpResponse('success', status=200)
    return HttpResponse('error', status=400)
        

    


