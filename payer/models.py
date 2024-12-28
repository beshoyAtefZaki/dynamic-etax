from django.db import models
from django.contrib.auth.models import User
# Create your models here.

versions = [("1.0" , "1.0") , ("0.9" , "0.9") ]
environment_choices = [("Production" , "Production") , ("Pre Production" , "Pre Production") ]
class PayerAccount(models.Model):
    user                          = models.ManyToManyField(User , null=True , blank=True )
    tax_id                        = models.CharField(max_length= 100, null=True , blank=True)
    user_token                    = models.CharField(max_length= 100 , null=True , blank=True)
    user_key                      = models.CharField(max_length= 100, null=True , blank=True)
    token_key                     = models.CharField(max_length=100, null=True , blank=True)
    issuer_type                   = models.CharField(max_length=100 , null=True , blank=True)
    issuer_id                     = models.CharField(max_length=100, null=True , blank=True)
    issuer_name                   = models.CharField(max_length=100, null=True , blank=True)
    issuer_address_branchId       = models.CharField(max_length=100, null=True , blank=True )
    issuer_address_country        = models.CharField(max_length=100, null=True , blank=True)
    issuer_address_governate      = models.CharField(max_length=100, null=True , blank=True)
    issuer_address_regionCity     = models.CharField(max_length=100, null=True , blank=True)
    issuer_address_street         = models.CharField(max_length=100, null=True , blank=True)
    issuer_address_buildingNumber = models.CharField(max_length=100, null=True , blank=True)
    activty_number                = models.CharField(max_length=100, null=True , blank=True)
    documentTypeVersion           = models.CharField(max_length=100,choices=versions,
                                                         null=True , blank=True)
    environment                   = models.CharField(max_length=100, null=True ,
                                                     blank=True,choices=environment_choices)
    # Add fields to token 
    lib                           = models.CharField(max_length=100, null=True , blank=True ,default = "C:/Windows/System32/eps2003csp11.dll")
    token_label                   = models.CharField(max_length=100, null=True , blank=True , default = "Egypt Trust")
    user_pin                      = models.CharField(max_length=100, null=True , blank=True)