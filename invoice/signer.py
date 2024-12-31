# required backages 

import json 
import hashlib
from http.client import HTTPSConnection
# import OpenSSL
from base64 import b64encode
import base64
import ssl
import sys
import requests
import datetime
from payer.models import PayerAccount
from reports.views import get_token


from pathlib import Path
import os
# lib = pkcs11.lib('C:/Windows/System32/eps2003csp11.dll')
from payer.utils import get_payer_account
Acocunt = get_payer_account() 
PAYER_ACCOUNT = Acocunt.get("Account")
login_url     =  Acocunt.get("url")#'id.eta.gov.eg' if PAYER_ACCOUNT.environment == "Production" else 'id.preprod.eta.gov.eg'
api_url       = Acocunt.get("api_url")       #'api.invoicing.eta.gov.eg' if PAYER_ACCOUNT.environment == "Production" else 'api.preprod.invoicing.eta.gov.eg'

method= '/connect/token'

def load_auther_data(inv):
   
   
    
   
  
    tok = get_token()
    headers = {
                    "Authorization"   : 'Bearer %s'%tok,
                    "Accept"          : "application/json" ,
                    "Accept-Language" : "ar" ,
                    'Content-Type'    :'application/json' 
                    }
    try :
        c = HTTPSConnection( api_url ,context=ssl._create_unverified_context())
        c.request('POST', '/api/v1.0/documentsubmissions' ,headers=headers , body=json.dumps(inv))
        res = c.getresponse()
        print(res.status, res.reason)
        data_r = res.read()
        if res.status == 202 :
            data = json.loads(data_r)
            accepted = data.get("acceptedDocuments")
            rejected = data.get("rejectedDocuments")
            return ({"Success":data})
        if res.status != 202 :
            return {"Token Error" : {"status" :str(res.status)  , "Error" :str( data_r)}}
    except Exception as E :
         return {"Token Error" : str(E) }
def concat_function(objects):
        ob = objects
        obj_str = ''
        for k , v in ob.items() : 
            obj_str = obj_str +f'"{k.upper()}"'
            if k in ["issuer" , "receiver"] :
                for a ,b in v.items()  :
                    obj_str = obj_str + f'"{a.upper()}"'
                    if a != "address" :
                        obj_str += f'"{b}"'
                    if a == "address" :
                        for c,d in b.items():
                            obj_str = obj_str +f'"{c.upper()}"' + f'"{d}"'
            if k not in ["issuer" , "receiver" , "invoiceLines" , "taxTotals"] :
                obj_str = obj_str + f'"{v }"'
            if k == "invoiceLines" :
                for line in v :
                    for a,b in line.items() :
                        obj_str =obj_str +f'"{a.upper()}"'
                        if a not in ["unitValue" , "discount" ,"taxableItems"] :
                            obj_str = obj_str + f'"{b}"'
                        if a in ["discount" , "unitValue"] :
                            for c ,d in b.items() :
                                obj_str = obj_str +f'"{c.upper()}"' + f'"{d}"'
                        if a in ["taxableItems"]  :
                            if len(b) == 0 :
                                obj_str = obj_str + ""
                            if len(b) > 0 :
                            
                                for e in b :
                                    for f,g in e.items() :
                                        obj_str = obj_str +f'"{f.upper()}"' + f'"{g}"'

            if k =="taxTotals" :
                if len(v)>  0 :
                    for a in v :
                        for f,g in a.items() :
                             obj_str = obj_str +f'"{f.upper()}"' + f'"{g}"'
                if len(v) == 0 :
                    obj_str = obj_str + ""
        return(obj_str)


BASE_DIR = Path(__file__).resolve().parent.parent

class Signer:
    """
    data to init 
    lib path = 'C:/Windows/System32/eps2003csp11.dll'
    token labe = Egypt Trust or user token name 
    user_pin = token pin 

    """
   

# test here 
# a =Signer(
#     'C:/Windows/System32/eps2003csp11.dll' , 'Egypt Trust' , "D@123456"
# )
# inv =  {'documents':[
#             {"issuer": {"name": "Dynamic Business Solutions", "id": "636346196", "type": "B", 
#         "address": {"branchID": "0", "country": "EG", "governate": "Cairo",
#         "regionCity": "Cairo",
#         "street": "ahmed", "buildingNumber": "1"}},
#     "receiver": {"name": "KVRD", "id": "533057086", "type": "B",
#         "address": {"branchID": "0", "country": "EG", 
#         "governate": "hass", 
#         "regionCity": "cairo", "street": "mohsien", 
#         "buildingNumber": "600"}}, "documentType": "i", "documentTypeVersion": "1.0",
#         "dateTimeIssued": "2022-11-13T11:15:32Z", "taxpayerActivityCode": "6201",
#         "internalID": "5555555555", "purchaseOrderReference": "nan", "purchaseOrderDescription": "", 
#         "salesOrderReference": "nan", "salesOrderDescription": "", "proformaInvoiceNumber": "", 
#         "invoiceLines": 
#       [{"description": "Desc Item", "itemType": "EGS", "itemCode": "EG-636346196-110006",
#        "unitType": "EA", "quantity": 1.0, "internalCode": "EG-636346196-110006", 
#        "salesTotal": 22104.0, "total": 2523.96, "valueDifference": 0.0, "totalTaxableFees": 0.0, 
#        "netTotal": 22104.0, "itemsDiscount": 0, 
#        "unitValue": {"currencySold": "EGP", "amountEGP": 20214.0, "amountSold": 0, 
#        "currencyExchangeRate": 0}, "discount": {"rate": 0, "amount": 0.0}, 
#        "taxableItems": [{"taxType": "T1", "amount": 309.96, "subType": "V009", "rate": 14.0}]}],
#         "totalDiscountAmount": 0.0, "totalSalesAmount": 2214.0, "netAmount": 2214.0,
#          "taxTotals": [{"taxType": "T1", "amount": 309.96}], "totalAmount": 2523.96,
#           "extraDiscountAmount": 0.0, "totalItemsDiscountAmount": 0}


# ]}

# a.sign_documents(inv)