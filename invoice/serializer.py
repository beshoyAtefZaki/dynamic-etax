

from .models import EInvoice , InvoiceLine

from rest_framework import serializers


# Model Fro serialziers 
from item.models import Item
from home.models import UOM 


from tax.models import taxableItems , TaXCategory , TaxTotals
# Create Serializer To invocie line \



# Item Get And Post Serializer 
class TaXCategorySerializer(serializers.ModelSerializer) :
    class Meta:
        model  = TaXCategory
        fields = '__all__'

class TaxableItemsSerializer(serializers.ModelSerializer):
    class Meta :
        model = taxableItems
        fields = '__all__'

class InvoiceLineSerializer(serializers.ModelSerializer):
    unitType  = serializers.ChoiceField(choices=UOM)
    taxableItems = TaxableItemsSerializer(many =True)
    tax_cat  = TaXCategorySerializer()
    class Meta :
        model = InvoiceLine
        fields = '__all__' 



class InvoiceSerializers(serializers.ModelSerializer):
    invoiceLines =  InvoiceLineSerializer(many =True )
    class Meta:
        model = EInvoice
        fields = '__all__'