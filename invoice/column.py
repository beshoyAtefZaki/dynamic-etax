from payer.models import PayerAccount
import subprocess
import pandas as pd
import json
import requests
from .models import EInvoice
from tax.models import TaXCategory, taxableItems ,TaxTotals
from http.client import HTTPSConnection
from base64 import b64encode
import ssl
import os
import numpy as np
from .signer import Signer

from payer.utils import get_payer_account
Acocunt = get_payer_account() 
PAYER_ACCOUNT = Acocunt.get("Account")
login_url     =  Acocunt.get("url")#'id.eta.gov.eg' if PAYER_ACCOUNT.environment == "Production" else 'id.preprod.eta.gov.eg'
api_url       = Acocunt.get("api_url")    
     
   
columns = ['Series',
'Type',
'Document Type',
'Receiver Type',
'Receiver',
'Receiver Id',
'Receiver Name',
'Receiver branchID',
'Receiver Country',
'Receiver Region City',
'Receiver Governate',
'Receiver Street',
'Receiver Building Number',
'Date TimeIssued',
'Internal Id',
'Sales Order Reference',
'Purchase Order Reference',
'Extra Discount Amount'
           ]

items_cols = [
                'Code (Item)',
                'Description (Item)',
                'UOM (Item)',
                'Item Type (Item)',
                'QTY (Item)',
                'Rate (Item)',
                'Discount (Item)',
                'Item Tax (Item)',
                'amountSold(Item)' ,
                'currencySold(Item)' , 
                'currencyExchangeRate(Item)' , 
                'Tax Amount' 
                ]



def create_full_documents(li ):
    forms =  { "documents": []}
    for id in li : 
        invoice  = EInvoice.objects.filter(id=id).first()
        if not invoice :
            return ({'error' : "Invocie Id Error "})
        form = {
            
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
                                                "id"     : invoice.receiver_id if invoice.receiver_id !='nan' else '',
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
                    "documentTypeVersion"      :str(invoice.documentTypeVersion), 
                    # 2021-05-17 12:21:11
                    "dateTimeIssued"            :invoice.datetimestr ,
                    "taxpayerActivityCode"     : str(invoice.taxpayerActivityCode ) ,
                    "internalID"               : str(invoice.internalId or ''),
                    "purchaseOrderReference"   : str(invoice.purchaseOrderReference or ''),
                    "purchaseOrderDescription" : "" ,
                    "salesOrderReference"      : str(invoice.salesOrderReference or '') ,
                    "salesOrderDescription"    : "" ,
                    "proformaInvoiceNumber"    : "" ,
                    # "delivery"                 : str(invoice.delivery or ''),
                    

                    #Item section 
                    "invoiceLines" :[ {
                                'description'     :item.description,
                                'itemType'        :item.itemType,
                                'itemCode'        :item.itemCode,
                                'unitType'        :item.unitType,
                                'quantity'        :float(item.quantity),
                                'internalCode'    :item.itemCode,
                                'salesTotal'      :round(float(item.salesTotal or 0 ) ,5),
                                'total'           :round( float(item.total or 0) , 5) ,
                                'valueDifference' :float(item.valueDifference or 0) , 
                                'totalTaxableFees':round(float(item.totalTaxableFees or 0 ) , 5) ,#float(item.total_taxable_fees or 0),
                                'netTotal'        :round(float(item.netTotal or 0) , 5 )  ,
                                'itemsDiscount'   : 0, #round((item.item_discount * item.quantity) , 5),
                                'unitValue'       :   {
                                                        'currencySold'        :item.unitValue_currencySold,
                                                        'amountEGP'           :round(float(item.unitValue_amountEGP) , 5),
                                                        'amountSold'          :round(float(item.unitValue_amountSold or 0) , 5) if item.unitValue_currencySold != 'EGP' else 0,
                                                        'currencyExchangeRate': round(float(item.unitValue_currencyExchangeRate or 1 ) , 5) if item.unitValue_currencySold != 'EGP' else 0,
                                                        },
                                'discount'        :  {
                                                    'rate':0,
                                                        'amount':round((float(item.discount_amount  or 0)  ), 5)
                                                        },

                                    "taxableItems" :[ {"taxType":tax_i.taxType ,
                                                    "amount": abs(round(float(tax_i.amount or 0 ) , 5)) ,
                                                        "subType" : tax_i.subType ,
                                                        "rate" :abs(round( float ( tax_i.rate or 0) , 5 ))}
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
                            "amount" : abs(round( float (tax_e.amount or 0),5))
                        }
                    for tax_e in  
                    invoice.taxTotals.all()],#invoice.taxTotals.all(),
                    "totalAmount"              :float(invoice.totalAmount or 0)  -float(invoice.extraDiscountAmount or 0) ,
                    "extraDiscountAmount"      :float(invoice.extraDiscountAmount or 0),  #extraDiscountAmount
                    "totalItemsDiscountAmount" :0 ,

            }
        forms["documents"].append(form) 
    # print(forms)
    PAYER_ACCOUNT = PayerAccount.objects.first()
    a =Signer(
    PAYER_ACCOUNT.lib , PAYER_ACCOUNT.token_label , PAYER_ACCOUNT.user_pin
            )

    response = a.sign_documents(forms)
    error = response.get("Token Error")
    success = response.get("Success")
    if error :
        for id in li : 
                 invoice  = EInvoice.objects.filter(id=id).first()
                 invoice.message_Serv =error
                 invoice.status = "Not Send"
                 invoice.save()
        print(f"Catch ---- {error}") 

        return ({"Error" : str(error)})

    
    submissionId = success.get("submissionId")
    accepted     = success.get("acceptedDocuments")
    if len(accepted) > 0 :
        for accepte in accepted :
            #update invocie status and longind and submition id 
            number = accepte.get("internalId")
            invocie = EInvoice.objects.filter(internalId = number)
            for i in invocie :
                i.submissionId = submissionId
                i.uuid = accepte.get('uuid')
                i.long_id = accepte.get('longId')
                i.message_Serv = accepte.get('uuid')
                i.status= "Submitted"
                i.save()
    rejected     = success.get("rejectedDocuments")
    if len(rejected) > 0 :
        for reject in rejected :
             number = reject.get("internalId")
             error = reject.get("error")
             details = error.get("details")
             messagage = ""
             for mes in details :
                messagage = messagage + mes.get("message") + '\n'
             invocie = EInvoice.objects.filter(internalId = number)
             for i in invocie :
                i.message_Serv = messagage
                i.save()
   
    return {"Accepted" :accepted or []  , "rejected" : rejected or [], "error" : str(error or " ") , "submissionId" :str(submissionId or " ") }
""" 
{'Success': {'submissionId': '98SB193AXB3BGXE2HZG003JG10', 'acceptedDocuments': 
[{'uuid': 'KX5NF48ZJSYYH3KHHZG003JG10', 'longId': 'HT4B5QR6E6NF9JNFHZG003JG10anhgfb1668695475', 
'internalId': 'a-15444', 'hashKey': 'Mdo1zUdSk5YkOWaScYcwAjPt+efuOdijNuXN1W5qQeM='}],
 'rejectedDocuments': []}}

"""
    
    




        

def post_to_auth_upload(id):
    
    from reports.views import get_token
    invoice  = EInvoice.objects.filter(id=id).first()
    if not invoice :
        return ({'error' : "Invocie Id Error "})
    
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
									 "id"     : invoice.receiver_id if invoice.receiver_id !='nan' else '',
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
        "documentTypeVersion"      :str(invoice.documentTypeVersion), 
        # 2021-05-17 12:21:11
        "dateTimeIssued"            :invoice.datetimestr ,
        "taxpayerActivityCode"     : str(invoice.taxpayerActivityCode ) ,
        "internalID"               : str(invoice.internalId or ''),
        "purchaseOrderReference"   : str(invoice.purchaseOrderReference or ''),
        "purchaseOrderDescription" : "" ,
        "salesOrderReference"      : str(invoice.salesOrderReference or '') ,
        "salesOrderDescription"    : "" ,
        "proformaInvoiceNumber"    : "" ,
        # "delivery"                 : str(invoice.delivery or ''),
        

        #Item section 
        "invoiceLines" :[ {
		              'description'     :item.description,
		              'itemType'        :item.itemType,
		              'itemCode'        :item.itemCode,
		              'unitType'        :item.unitType,
		              'quantity'        :float(item.quantity),
		              'internalCode'    :item.itemCode,
		              'salesTotal'      :round(float(item.salesTotal or 0 ) ,5),
		              'total'           :round( float(item.total or 0) , 5) ,
		              'valueDifference' :float(item.valueDifference or 0) , 
		              'totalTaxableFees':round(float(item.totalTaxableFees or 0 ) , 5) ,#float(item.total_taxable_fees or 0),
		              'netTotal'        :round(float(item.netTotal or 0) , 5 )  ,
		              'itemsDiscount'   : 0, #round((item.item_discount * item.quantity) , 5),
		              'unitValue'       :   {
		                                    'currencySold'        :item.unitValue_currencySold,
		                                    'amountEGP'           :round(float(item.unitValue_amountEGP) , 5),
		                                    'amountSold'          :round(float(item.unitValue_amountSold or 0) , 5) if item.unitValue_currencySold != 'EGP' else 0,
		                                    'currencyExchangeRate': round(float(item.unitValue_currencyExchangeRate or 1 ) , 5) if item.unitValue_currencySold != 'EGP' else 0,
		                                    },
		              'discount'        :  {
		                                   'rate':0,
		                                    'amount':round((float(item.discount_amount  or 0)  ), 5)
		                                    },

                        "taxableItems" :[ {"taxType":tax_i.taxType ,
                                           "amount": abs(round(float(tax_i.amount or 0 ) , 5)) ,
                                            "subType" : tax_i.subType ,
                                            "rate" :abs(round( float ( tax_i.rate or 0) , 5 ))}
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
                "amount" : abs(round( float (tax_e.amount or 0),5))
            }
        for tax_e in  
        invoice.taxTotals.all()],#invoice.taxTotals.all(),
        "totalAmount"              :float(invoice.totalAmount or 0)  -float(invoice.extraDiscountAmount or 0) ,
        "extraDiscountAmount"      :float(invoice.extraDiscountAmount or 0),  #extraDiscountAmount
        "totalItemsDiscountAmount" :0 ,


		


    }]
    }
    form2 = form
    token = get_token()
    headers = {
				"Authorization"   : 'Bearer %s'%token,
				"Accept"          : "application/json" ,
				"Accept-Language" : "ar" ,
				'Content-Type'    :'application/json' 
				 }

    import sys
    
    if invoice.documentTypeVersion == "0.9"  :
        #print("3-",invoice.documentTypeVersion )
        c = HTTPSConnection('api.preprod.invoicing.eta.gov.eg' ,context=ssl._create_unverified_context())
        c.request('POST', '/api/v1.0/documentsubmissions' ,headers=headers , body=json.dumps(form) )
        res = c.getresponse()
        data = res.read()
        data = json.loads(data)   
        return (

            {"message" : data ,"invoice":form}
            )
    if invoice.documentTypeVersion == "1.0"  :
        #print("formmmmmmmmmmmmmyyyyyy",form)
        main_data={}
        try :
          os.remove('C:/j/sFile.txt')
        except:
            pass
        jsonfile = "C:/j/sFile.txt"
        str_form = json.dumps(form.get('documents')[0])
        #print(" form" , str_form)
        with open(jsonfile, 'a', encoding='utf-8') as outfile:
            json.dump(form.get('documents')[0], outfile )

        cmd = 'C:/j/EInvoicingSigner.exe'
        result = subprocess.Popen([cmd ,' '], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        a,b = result.communicate()
        h = {"id" :invoice.id }
        #print(a,b)
        if a :
            
            try :
                a = str(a)
                pre_s = a.split("{")[0]
                a = a.replace(pre_s,'')
                post_x = a.split("}")[-1]
                a = a.replace(post_x,'')
                spec_chars = ["\\r","\\n"]
                for spec_x in spec_chars :
                    a = a.replace(spec_x,'')
                r = json.loads(a)
                if r.get("submissionId") :
                     h["submissionId"] =   r.get("submissionId")
                     h["uuid"] = r.get("acceptedDocuments")[0].get("uuid") if len(r.get("acceptedDocuments")) > 0 else None
                     h["long_id"] = r.get("acceptedDocuments")[0].get("longId") if len(r.get("acceptedDocuments"))  > 0 else None
                if not r.get("submissionId") :
                    h["message_Serv"] = str(a) + str(b)
                r = requests.post("http://127.0.0.1:8005/main/post_update_status" , h)
            except Exception as e :
                h["message_Serv"] = f"' {a}, {b}' '"
                r = requests.post("http://127.0.0.1:8005/main/post_update_status" ,h)
                print ("error wihle loads json from signer =====> " , str(e))
        else :
             print(f"____________________ {b} ____________________")
             h["message_Serv"] =f" {b} "
             r = requests.post("http://127.0.0.1:8005/main/post_update_status" ,h)
        return {"message" :h}





def e_invoice_form(data):

        invoice = data
        ic_invoice = EInvoice()
        issuer                                   = invoice.get('issuer')
        ic_invoice.uploader_id                   = str(invoice.get('uploader_id'))
        ic_invoice.issuer_type                   = issuer.get('issuer_type')
        ic_invoice.issuer_id                     = issuer.get('issuer_id')
        ic_invoice.issuer_name                   = issuer.get('issuer_name')
        address                                  = issuer.get('address')
        ic_invoice.issuer_address_branchId       = address.get('branchID')
        ic_invoice.issuer_address_country        = address.get('country')
        ic_invoice.issuer_address_governate      = address.get('governate')
        ic_invoice.issuer_address_regionCity     = address.get('regionCity')
        ic_invoice.issuer_address_street         = address.get('street')
        ic_invoice.issuer_address_buildingNumber = address.get('buildingNumber')
        ic_invoice.receiver_type                   = invoice.get('Receiver Type')
        ic_invoice.receiver_id                     = str(invoice.get('Receiver Id')).split('.')[0]
        ic_invoice.receiver_name                   = invoice.get('Receiver Name') or ''
        
        # receiver_address                           = invoice.get('receiver_address')
        ic_invoice.receiver_address_branchId       = str(invoice.get('Receiver branchID')).split('.')[0]
        ic_invoice.receiver_address_country        = invoice.get('Receiver Country')
        ic_invoice.receiver_address_governate      = invoice.get('Receiver Governate')
        ic_invoice.receiver_address_regionCity     = invoice.get('Receiver Region City')
        ic_invoice.receiver_address_street         = invoice.get('Receiver Street')
        ic_invoice.receiver_address_buildingNumber = str(invoice.get('Receiver Building Number')).split('.')[0]
        ic_invoice.rd_tax                          = invoice.get('rd_tax')
       
        # set document info 
        ic_invoice.internalId   = invoice.get('Internal Id')
        ic_invoice.datetimestr  = invoice.get('Date TimeIssued')
        ic_invoice.documentType = invoice.get('Document Type')
        ic_invoice.documentTypeVersion= str(issuer.get('documentTypeVersion'))
        ic_invoice.taxpayerActivityCode = invoice.get('taxpayerActivityCode')
      
        ic_invoice.salesOrderReference = invoice.get('Sales Order Reference')if invoice.get('Sales Order Reference') else " "
        
        ic_invoice.purchaseOrderReference = invoice.get('Purchase Order Reference') if invoice.get('Purchase Order Reference') else " "
        try :
            ic_invoice.extraDiscountAmount = 0 #float(invoice.get('Extra Discount Amount') or 0) if not np.isnan(invoice.get('Extra Discount Amount')) else 0
        except :
            ic_invoice.extraDiscountAmount = 0 
        
        # ic_invoice.deliveryr_str Id = str(invoice.get('Internal Id')).split('.')[0]

        ic_invoice.save()
        #set Invoice Items 
        invoiceLines = invoice.get('items')
        for line in invoiceLines :
            taxes = line.get('Item Tax (Item)')
            # # taxes_list = [{tax.}]
            tax_cat =  TaXCategory.objects.filter(name =taxes).first()
            currency = line.get('currencySold(Item)')  
            exchangerate = 1 
            if float(line.get('currencyExchangeRate(Item)') or 1 )  != 1:
                 exchangerate = float(line.get('currencyExchangeRate(Item)') or 1 ) if not np.isnan(line.get('currencyExchangeRate(Item)')) else 1
            if  tax_cat :
                
                ic_invoice.invoiceLines.create(
                        
                        description = line.get('Description (Item)'),
                        itemType = line.get('Item Type (Item)'),
                        itemCode = line.get('Code (Item)'),
                        unitType = line.get('UOM (Item)') ,
                        quantity = float(line.get('QTY (Item)')),
                        unitValue_currencySold = currency,
                        unitValue_currencyExchangeRate =  float(exchangerate or 1 )if currency !="EGP" else 0  ,#float(line.get('currencyExchangeRate(Item)') or 0 ), 
                        unitValue_amountSold =round(float(line.get('Rate (Item)') or 0 ) ,5 ) if currency !="EGP" else 0 ,
                        unitValue_amountEGP  = round ((round(float(line.get('Rate (Item)') or 1 )  , 5) * float(exchangerate or 1) ) , 5 ),
                        parent_type = "EInvoice" ,
                        parent_id= ic_invoice.id,
                        tax_cat = tax_cat ,
                        discount_amount =float( line.get('Discount (Item)')),
                        rd_tax   = float(line.get('Tax Amount') or 0) if not np.isnan(line.get('Tax Amount')) else 0



                )
            else:
                ic_invoice.invoiceLines.create(
                    
                        description = line.get('Description (Item)'),
                        itemType = line.get('Item Type (Item)'),
                        itemCode = line.get('Code (Item)'),
                        unitType = line.get('UOM (Item)') ,
                        quantity = float(line.get('QTY (Item)')),
                        unitValue_currencySold = currency,
                        unitValue_currencyExchangeRate =  exchangerate ,#float(line.get('currencyExchangeRate(Item)') or 0 ), 
                        unitValue_amountSold =round(float(line.get('Rate (Item)') or 0 ) ,5 )  ,
                        unitValue_amountEGP  = round ((round(float(line.get('Rate (Item)') or 0 )  , 5) * exchangerate ) , 5 ),
                        parent_type = "EInvoice" ,
                        parent_id= ic_invoice.id,
                        discount_amount =float( line.get('Discount (Item)')),
                      



                )
          
            ic_invoice.save()
        tax_types = {}
        taxableitem = 0
        for line in ic_invoice.invoiceLines.all():
                total_taxes_fees = 0 
                if line.tax_cat :
                    for tax in  line.tax_cat.tax_table.all() :
                        rate =tax.rate 
                        amount = tax.amount
                        if tax.rate and tax.rate != 0  :
                            amount = (float(line.unitValue_amountEGP or 0) - float(line.discount_amount or 0 )) * (float(rate) / 100 )
                        elif tax.subType in ["RD02" , "ST02" , "RD04"] :
                            amount = float(line.rd_tax or 0)
                            total_taxes_fees += amount
                        if  tax.subType != "ST02":
                            amount=  float(amount or 0) * float(line.quantity or 0)

                        in_tax = taxableItems(taxType = tax.taxType , rate = tax.rate ,
                        subType = tax.subType , amount = round(amount , 4)  , parent_id = line.id , parent_type = 'invoiceLines')
                        for k , v in tax_types.items() :
                                if k ==  tax.taxType :
                                    tax_types[k] = float(v) + float(amount)
                        if tax.taxType  not in  tax_types.keys() :
                            tax_types[tax.taxType] = float(amount) 
                        in_tax.save()
                        line.totalTaxableFees = total_taxes_fees
                        taxableitem += total_taxes_fees
                        line.taxableItems.add(in_tax)
                        line.save()
        ic_invoice.taxableitem = taxableitem
        for k,v in tax_types.items() :
            a =TaxTotals(taxType = k , amount = v , parent_id = ic_invoice.id , parent_type = "EInvoice" )
            a.save()
            ic_invoice.taxTotals.add(a)
            ic_invoice.save()
        return ic_invoice.id
        # import threading
        # ic_invoice.save()
        # processThread = threading.Thread(target=post_to_auth_upload, args=((ic_invoice.id,)) ) # <- note extra ','
        # processThread.start()
        # processThread.join()
    





        return ({"acction" : "proccess"} )


from payer.models import PayerAccount
def create_e_invoice(data):
    invoice = data

    ic_invoice = EInvoice()
    # issuer = invoice.get('issuer')
    # ic_invoice.uploader_id = str(invoice.get('uploader_id'))
    issuer = PayerAccount.objects.all().first()
    print("issuerrr",issuer)
    ic_invoice.issuer_type = issuer.issuer_type
    ic_invoice.issuer_id = issuer.issuer_id
    ic_invoice.issuer_name = issuer.issuer_name
    # address = issuer.get('address')
    ic_invoice.issuer_address_branchId =issuer.issuer_address_branchId
    ic_invoice.issuer_address_country = issuer.issuer_address_country
    ic_invoice.issuer_address_governate = issuer.issuer_address_governate
    ic_invoice.issuer_address_regionCity = issuer.issuer_address_regionCity
    ic_invoice.issuer_address_street = issuer.issuer_address_street
    ic_invoice.issuer_address_buildingNumber = issuer.issuer_address_buildingNumber
    ic_invoice.receiver_type = invoice.get('receiver_type')
    ic_invoice.receiver_id = str(invoice.get('receiverid')).split('.')[0]
    ic_invoice.receiver_name = invoice.get('receivername') or ''
    # receiver_address                           = invoice.get('receiver_address')
    ic_invoice.receiver_address_branchId = str(invoice.get('branchid')).split('.')[0]
    ic_invoice.receiver_address_country = invoice.get('country_code')
    ic_invoice.receiver_address_governate = invoice.get('governate')
    ic_invoice.receiver_address_regionCity = invoice.get('regioncity')
    ic_invoice.receiver_address_street = invoice.get('street')
    ic_invoice.receiver_address_buildingNumber = str(invoice.get('buildingnumber')).split('.')[0]

    # set document info
    ic_invoice.datetimestr = invoice.get('datetime_issued')
    ic_invoice.dateTimeIssued=invoice.get('datetime_issued')
    ic_invoice.documentType = invoice.get('document_type')
    ic_invoice.documentTypeVersion = str(issuer.documentTypeVersion)
    ic_invoice.taxpayerActivityCode = issuer.activty_number
    ic_invoice.internalId = str(invoice.get('internalid')).split('.')[0]
    ic_invoice.save()
    # set Invoice Items
    invoiceLines =invoice.get('items') #json.loads()
    for line in invoiceLines:
        taxes = line.get('item_tax_template')
        # # taxes_list = [{tax.}]
        print("line.get('item_tax_template')",line.get('item_tax_template'))
        print("taxes",taxes)
        tax_cat = TaXCategory.objects.filter(name=taxes).first()
        print("taxxxxx",tax_cat)
        if not tax_cat:
            print( "Not valid tax catigory" , taxes)
            pass
            # return {'error': "Not valid tax catigory"}
        # unitValue = line.get('unitValue')
        ic_invoice.invoiceLines.create(

            description=line.get('description'),
            itemType=line.get('item_type'),
            itemCode=line.get('item_code'),
            unitType=line.get('uom'),
            quantity=float(line.get('qty')),
            unitValue_currencySold='EGP',
            unitValue_amountEGP=round(float(line.get('rate') or 0), 4),
            parent_type="EInvoice",
            parent_id=ic_invoice.id,
            tax_cat=tax_cat,
            discount_amount=float(line.get('discount_amount'))

        )
        ic_invoice.save()
    tax_types = {}
    for line in ic_invoice.invoiceLines.all():

        for tax in line.tax_cat.tax_table.all():
            rate = tax.rate
            amount = tax.amount
            if tax.rate and tax.rate > 0:
                amount = ((float(rate) / 100) * (float(line.unitValue_amountEGP or 0))) - float(
                    line.discount_amount or 0)

            amount = amount * float(line.quantity or 0)
            print(amount)
            in_tax = taxableItems(taxType=tax.taxType, rate=tax.rate,
                                  subType=tax.subType, amount=round(amount, 4), parent_id=line.id,
                                  parent_type='invoiceLines')
            for k, v in tax_types.items():
                if k == tax.taxType:
                    tax_types[k] = float(v) + float(amount)
            if tax.taxType not in tax_types.keys():
                tax_types[tax.taxType] = float(amount)

            in_tax.save()
            line.taxableItems.add(in_tax)
            line.save()
    for k, v in tax_types.items():
        a = TaxTotals(taxType=k, amount=v, parent_id=ic_invoice.id, parent_type="EInvoice")
        a.save()
        ic_invoice.taxTotals.add(a)
        ic_invoice.save()
  
    response = post_to_auth_upload(ic_invoice.id)
    print("response",response)
    ic_invoice.message_Serv = response
    ic_invoice.save()

    return (response)


def create_request(uploader_id , pth):
    """
    this function take file to read it in pandas 
    """

    print("Stop here")
    data = pd.read_excel( pth  ,sheet_name = 0)
    dat_list = []
    dict_data = {}
    for id in range(0 , len(data['Code (Item)'])) :
       
        items_list = []
        items_data = {}
        try :
            idxc =  data['Internal Id'].iloc[id] 
        except:
            return {"erro" : 'Plaes set Internal id correctly'}
        if  str(data['Internal Id'].iloc[id]) !='nan' and data['Internal Id'].iloc[id] :
            items_list = []
            dict_data = {}
            for col_name in columns :
                try :
                     dict_data[col_name] = data[col_name].iloc[id] if data[col_name].iloc[id] != 'nan' else " "
                except:
                    print ({"erro" : col_name +'  - not found'})
                    pass
           
            for item in items_cols :
                
                if item in data.keys():
                    items_data[item] = data[item].iloc[id]  
            items_list.append(items_data)
           
            if len(items_list) > 0 :
                dict_data['items'] = items_list
                dat_list.append(dict_data)
        
        if  str(data['Internal Id'].iloc[id]) =='nan' and str(data['Code (Item)'].iloc[id] )!= 'nan' :
            items_data ={}
            for item in items_cols :
                items_data[item] = data[item].iloc[id]  
            items_list.append(items_data)
            if len(items_list) > 0 :
                for i in items_list : 
                  dict_data['items'].append (i)
    response_datat = []
    issuer = PayerAccount.objects.all().first()
    if not issuer :
            print ({"error " : "No Issuer Account Found !"})
   
    issr    = {                              
            "issuer_type"                 :  issuer.issuer_type,
            "issuer_id"                   :   str(issuer.issuer_id),
            "issuer_name"                   : issuer.issuer_name,
            "address"   :{                             
                        "branchID"       :  str(issuer.issuer_address_branchId)  ,
                        "country"        : issuer.issuer_address_country ,
                        "governate"      : issuer.issuer_address_governate,
                        "regionCity"     : issuer.issuer_address_regionCity,
                        "street "        : issuer.issuer_address_street ,
                        "buildingNumber" : str( issuer.issuer_address_buildingNumber)
                        },
            "documentTypeVersion" : str(issuer.documentTypeVersion)
                        
                        
                    } 
    invocies = []
    for inv in dat_list :
       inv['issuer'] = issr
       inv['taxpayerActivityCode'] = str(issuer.activty_number)
       inv['uploader_id'] = str(uploader_id)
       r_str = str(inv).replace("'" , '"') 
       r_str = str(r_str).replace("nan" , ' " " ')
       status = e_invoice_form(inv)
       invocies.append(status)
    
    message = []
    for e_invoice  in invocies :
       a =  post_to_auth_upload(e_invoice)
       message.append(a)
  
    return { "message" : message}