from  .models import PayerAccount


def get_payer_account():
    # global PAYER_ACCOUNT ,url ,api_url
    obj = {
        "Account" : "" ,
         "url" : "" ,
        "api_url" : ""
    }
    try :
        payers = PayerAccount.objects.all()
        if len(payers) > 0  :
            PAYER_ACCOUNT =  payers.first()
            obj["account"] = PAYER_ACCOUNT
            obj["url"] = 'id.eta.gov.eg' if PAYER_ACCOUNT.environment == "Production" else 'id.preprod.eta.gov.eg'
            obj["api_url"] = 'api.invoicing.eta.gov.eg' if PAYER_ACCOUNT.environment == "Production" else 'api.preprod.invoicing.eta.gov.eg'
            return obj
        else :
            return obj
    except :
        return obj