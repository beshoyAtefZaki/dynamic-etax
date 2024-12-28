# Generated by Django 3.2.5 on 2023-01-23 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountObj',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(blank=True, max_length=10, null=True)),
                ('description', models.CharField(blank=True, max_length=80, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Header',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('postingdate', models.DateTimeField(blank=True, null=True)),
                ('dateTimeIssued', models.CharField(blank=True, max_length=80, null=True)),
                ('receiptNumber', models.CharField(blank=True, max_length=80, null=True)),
                ('uuid', models.CharField(blank=True, max_length=80, null=True)),
                ('previousUUID', models.CharField(blank=True, max_length=80, null=True)),
                ('referenceOldUUID', models.CharField(blank=True, max_length=80, null=True)),
                ('currency', models.CharField(blank=True, choices=[('AED', 'UAE Dirham'), ('AFN', 'Afghani'), ('ALL', 'Lek'), ('AMD', 'Armenian Dram'), ('ANG', 'Netherlands Antillean Guilder'), ('AOA', 'Kwanza'), ('ARS', 'Argentine Peso'), ('AUD', 'Australian Dollar'), ('AWG', 'Aruban Florin'), ('AZN', 'Azerbaijan Manat'), ('BAM', 'Convertible Mark'), ('BBD', 'Barbados Dollar'), ('BDT', 'Taka'), ('BGN', 'Bulgarian Lev'), ('BHD', 'Bahraini Dinar'), ('BIF', 'Burundi Franc'), ('BMD', 'Bermudian Dollar'), ('BND', 'Brunei Dollar'), ('BOB', 'Boliviano'), ('BOV', 'Mvdol'), ('BRL', 'Brazilian Real'), ('BSD', 'Bahamian Dollar'), ('BTN', 'Ngultrum'), ('BWP', 'Pula'), ('BYN', 'Belarusian Ruble'), ('BZD', 'Belize Dollar'), ('CAD', 'Canadian Dollar'), ('CDF', 'Congolese Franc'), ('CHE', 'WIR Euro'), ('CHF', 'Swiss Franc'), ('CHW', 'WIR Franc'), ('CLF', 'Unidad de Fomento'), ('CLP', 'Chilean Peso'), ('CNY', 'Yuan Renminbi'), ('COP', 'Colombian Peso'), ('COU', 'Unidad de Valor Real'), ('CRC', 'Costa Rican Colon'), ('CUC', 'Peso Convertible'), ('CUP', 'Cuban Peso'), ('CVE', 'Cabo Verde Escudo'), ('CZK', 'Czech Koruna'), ('DJF', 'Djibouti Franc'), ('DKK', 'Danish Krone'), ('DOP', 'Dominican Peso'), ('DZD', 'Algerian Dinar'), ('EGP', 'Egyptian Pound'), ('ERN', 'Nakfa'), ('ETB', 'Ethiopian Birr'), ('EUR', 'Euro'), ('FJD', 'Fiji Dollar'), ('FKP', 'Falkland Islands Pound'), ('GBP', 'Pound Sterling'), ('GEL', 'Lari'), ('GHS', 'Ghana Cedi'), ('GIP', 'Gibraltar Pound'), ('GMD', 'Dalasi'), ('GNF', 'Guinean Franc'), ('GTQ', 'Quetzal'), ('GYD', 'Guyana Dollar'), ('HKD', 'Hong Kong Dollar'), ('HNL', 'Lempira'), ('HRK', 'Kuna'), ('HTG', 'Gourde'), ('HUF', 'Forint'), ('IDR', 'Rupiah'), ('ILS', 'New Israeli Sheqel'), ('INR', 'Indian Rupee'), ('IQD', 'Iraqi Dinar'), ('IRR', 'Iranian Rial'), ('ISK', 'Iceland Krona'), ('JMD', 'Jamaican Dollar'), ('JOD', 'Jordanian Dinar'), ('JPY', 'Yen'), ('KES', 'Kenyan Shilling'), ('KGS', 'Som'), ('KHR', 'Riel'), ('KMF', 'Comorian Franc '), ('KPW', 'North Korean Won'), ('KRW', 'Won'), ('KWD', 'Kuwaiti Dinar'), ('KYD', 'Cayman Islands Dollar'), ('KZT', 'Tenge'), ('LAK', 'Lao Kip'), ('LBP', 'Lebanese Pound'), ('LKR', 'Sri Lanka Rupee'), ('LRD', 'Liberian Dollar'), ('LSL', 'Loti'), ('LYD', 'Libyan Dinar'), ('MAD', 'Moroccan Dirham'), ('MDL', 'Moldovan Leu'), ('MGA', 'Malagasy Ariary'), ('MKD', 'Denar'), ('MMK', 'Kyat'), ('MNT', 'Tugrik'), ('MOP', 'Pataca'), ('MRU', 'Ouguiya'), ('MUR', 'Mauritius Rupee'), ('MVR', 'Rufiyaa'), ('MWK', 'Malawi Kwacha'), ('MXN', 'Mexican Peso'), ('MXV', 'Mexican Unidad de Inversion (UDI)'), ('MYR', 'Malaysian Ringgit'), ('MZN', 'Mozambique Metical'), ('NAD', 'Namibia Dollar'), ('NGN', 'Naira'), ('NIO', 'Cordoba Oro'), ('NOK', 'Norwegian Krone'), ('NPR', 'Nepalese Rupee'), ('NZD', 'New Zealand Dollar'), ('OMR', 'Rial Omani'), ('PAB', 'Balboa'), ('PEN', 'Sol'), ('PGK', 'Kina'), ('PHP', 'Philippine Peso'), ('PKR', 'Pakistan Rupee'), ('PLN', 'Zloty'), ('PYG', 'Guarani'), ('QAR', 'Qatari Rial'), ('RON', 'Romanian Leu'), ('RSD', 'Serbian Dinar'), ('RUB', 'Russian Ruble'), ('RWF', 'Rwanda Franc'), ('SAR', 'Saudi Riyal'), ('SBD', 'Solomon Islands Dollar'), ('SCR', 'Seychelles Rupee'), ('SDG', 'Sudanese Pound'), ('SEK', 'Swedish Krona'), ('SGD', 'Singapore Dollar'), ('SHP', 'Saint Helena Pound'), ('SLL', 'Leone'), ('SOS', 'Somali Shilling'), ('SRD', 'Surinam Dollar'), ('SSP', 'South Sudanese Pound'), ('STN', 'Dobra'), ('SVC', 'El Salvador Colon'), ('SYP', 'Syrian Pound'), ('SZL', 'Lilangeni'), ('THB', 'Baht'), ('TJS', 'Somoni'), ('TMT', 'Turkmenistan New Manat'), ('TND', 'Tunisian Dinar'), ('TOP', 'Pa’anga'), ('TRY', 'Turkish Lira'), ('TTD', 'Trinidad and Tobago Dollar'), ('TWD', 'New Taiwan Dollar'), ('TZS', 'Tanzanian Shilling'), ('UAH', 'Hryvnia'), ('UGX', 'Uganda Shilling'), ('USD', 'US Dollar'), ('USN', 'US Dollar (Next day)'), ('UYI', 'Uruguay Peso en Unidades Indexadas (UI)'), ('UYU', 'Peso Uruguayo'), ('UYW', 'Unidad Previsional'), ('UZS', 'Uzbekistan Sum'), ('VED', 'Bolívar Soberano'), ('VES', 'Bolívar Soberano'), ('VND', 'Dong'), ('VUV', 'Vatu'), ('WST', 'Tala'), ('XAF', 'CFA Franc BEAC'), ('XAG', 'Silver'), ('XAU', 'Gold'), ('XBA', 'Bond Markets Unit European Composite Unit (EURCO)'), ('XBB', 'Bond Markets Unit European Monetary Unit (E.M.U.-6)'), ('XBC', 'Bond Markets Unit European Unit of Account 9 (E.U.A.-9)'), ('XBD', 'Bond Markets Unit European Unit of Account 17 (E.U.A.-17)'), ('XCD', 'East Caribbean Dollar'), ('XDR', 'SDR (Special Drawing Right)'), ('XOF', 'CFA Franc BCEAO'), ('XPD', 'Palladium'), ('XPF', 'CFP Franc'), ('XPT', 'Platinum'), ('XSU', 'Sucre'), ('XTS', 'Codes specifically reserved for testing purposes'), ('XUA', 'ADB Unit of Account'), ('XXX', 'The codes assigned for transactions where no currency is involved'), ('YER', 'Yemeni Rial'), ('ZAR', 'Rand'), ('ZMW', 'Zambian Kwacha'), ('ZWL', 'Zimbabwe Dollar')], default='EGP', max_length=80, null=True)),
                ('exchangeRate', models.FloatField(blank=True, max_length=10, null=True)),
                ('sOrderNameCode', models.CharField(blank=True, max_length=80, null=True)),
                ('orderdeliveryMode', models.CharField(blank=True, choices=[('FC', 'From the company place'), ('TO', 'Transport by others'), ('TC', 'Transported by the company')], default='FC', max_length=80, null=True)),
                ('grossWeight', models.FloatField(blank=True, max_length=10, null=True)),
                ('netWeight', models.FloatField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='itemData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internalCode', models.CharField(blank=True, max_length=80, null=True)),
                ('description', models.CharField(blank=True, max_length=80, null=True)),
                ('itemType', models.CharField(blank=True, choices=[('EGS', 'EGS'), ('GS1', 'GS1')], max_length=80, null=True)),
                ('itemCode', models.CharField(blank=True, max_length=80, null=True)),
                ('unitType', models.CharField(blank=True, choices=[('2Z', 'Millivolt ( mV )'), ('4K', 'Milliampere ( mA )'), ('4O', 'Microfarad ( microF )'), ('A87', 'Gigaohm ( GOhm )'), ('A93', 'Gram/Cubic meter ( g/m3 )'), ('A94', 'Gram/cubic centimeter ( g/cm3 )'), ('AMP', 'Ampere ( A )'), ('ANN', 'Years ( yr )'), ('B22', 'Kiloampere ( kA )'), ('B49', 'Kiloohm ( kOhm )'), ('B75', 'Megohm ( MOhm )'), ('B78', 'Megavolt ( MV )'), ('B84', 'Microampere ( microA )'), ('BAR', 'bar ( bar )'), ('BBL', 'Barrel (oil 42 gal.)'), ('BG', 'Bag ( Bag )'), ('BO', 'Bottle ( Bt. )'), ('BOX', 'Box'), ('C10', 'Millifarad ( mF )'), ('C39', 'Nanoampere ( nA )'), ('C41', 'Nanofarad ( nF )'), ('C45', 'Nanometer ( nm )'), ('C62', 'Activity unit ( AU )'), ('CA', 'Canister ( Can )'), ('CMK', 'Square centimeter ( cm2 )'), ('CMQ', 'Cubic centimeter ( cm3 )'), ('CMT', 'Centimeter ( cm )'), ('CS', 'Case ( Case )'), ('CT', 'Carton ( Car )'), ('CTL', 'Centiliter ( Cl )'), ('D10', 'Siemens per meter ( S/m )'), ('D33', 'Tesla ( D )'), ('D41', 'Ton/Cubic meter ( t/m3 )'), ('DAY', 'Days ( d )'), ('DMT', 'Decimeter ( dm )'), ('DRM', 'DRUM'), ('EA', 'each (ST) ( ST )'), ('FAR', 'Farad ( F )'), ('FOT', 'Foot ( Foot )'), ('FTK', 'Square foot ( ft2 )'), ('FTQ', 'Cubic foot ( ft3 )'), ('G42', 'Microsiemens per centimeter ( microS/cm )'), ('GL', 'Gram/liter ( g/l )'), ('GLL', 'gallon ( gal )'), ('GM', 'Gram/square meter ( g/m2 )'), ('GPT', 'Gallon per thousand'), ('GRM', 'Gram ( g )'), ('H63', 'Milligram/Square centimeter ( mg/cm2 )'), ('HHP', 'Hydraulic Horse Power'), ('HLT', 'Hectoliter ( hl )'), ('HTZ', 'Hertz (1/second) ( Hz )'), ('HUR', 'Hours ( hrs )'), ('IE', 'Number of Persons ( PRS )'), ('INH', 'Inch ( “” )'), ('INK', 'Square inch ( Inch2 )'), ('IVL', 'Interval'), ('JOB', 'JOB'), ('KGM', 'Kilogram ( KG )'), ('KHZ', 'Kilohertz ( kHz )'), ('KMH', 'Kilometer/hour ( km/h )'), ('KMK', 'Square kilometer ( km2 )'), ('KMQ', 'Kilogram/cubic meter ( kg/m3 )'), ('KMT', 'Kilometer ( km )'), ('KSM', 'Kilogram/Square meter ( kg/m2 )'), ('KVT', 'Kilovolt ( kV )'), ('KWT', 'Kilowatt ( KW )'), ('LB', 'pounds '), ('LTR', 'Liter ( l )'), ('LVL', 'Level'), ('M', 'Meter ( m )'), ('MAN', 'Man'), ('MAW', 'Megawatt ( VA )'), ('MGM', 'Milligram ( mg )'), ('MHZ', 'Megahertz ( MHz )'), ('MIN', 'Minute ( min )'), ('MMK', 'Square millimeter ( mm2 )'), ('MMQ', 'Cubic millimeter ( mm3 )'), ('MMT', 'Millimeter ( mm )'), ('MON', 'Months ( Months )'), ('MTK', 'Square meter ( m2 )'), ('MTQ', 'Cubic meter ( m3 )'), ('OHM', 'Ohm ( Ohm )'), ('ONZ', 'Ounce ( oz )'), ('PAL', 'Pascal ( Pa )'), ('PF', 'Pallet ( PAL )'), ('PK', 'Pack ( PAK )'), ('PMP', 'pump'), ('RUN', 'run'), ('SH', 'Shrink ( Shrink )'), ('SK', 'Sack'), ('SMI', 'Mile ( mile )'), ('ST', 'Ton (short,2000 lb)'), ('TNE', 'Tonne ( t )'), ('TON', 'Ton (metric)'), ('VLT', 'Volt ( V )'), ('WEE', 'Weeks ( Weeks )'), ('WTT', 'Watt ( W )'), ('X03', 'Meter/Hour ( m/h )'), ('YDQ', 'Cubic yard ( yd3 )'), ('YRD', 'Yards ( yd )')], max_length=80, null=True)),
                ('quantity', models.FloatField(blank=True, max_length=10, null=True)),
                ('unitPrice', models.FloatField(blank=True, max_length=10, null=True)),
                ('netSale', models.FloatField(blank=True, max_length=10, null=True)),
                ('totalSale', models.FloatField(blank=True, max_length=10, null=True)),
                ('total', models.FloatField(blank=True, max_length=10, null=True)),
                ('valueDifference', models.FloatField(blank=True, default=0, max_length=10, null=True)),
                ('parent', models.CharField(blank=True, max_length=80, null=True)),
                ('commercialDiscountData', models.ManyToManyField(blank=True, null=True, to='ereciept.DiscountObj')),
                ('itemDiscountData', models.ManyToManyField(blank=True, null=True, related_name='itemdiscout', to='ereciept.DiscountObj')),
            ],
        ),
        migrations.CreateModel(
            name='NewReceieptSerial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(blank=True, default='NEW-INV-', max_length=80, null=True)),
                ('name', models.CharField(blank=True, max_length=80, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReceieptSerial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(blank=True, default='SAL-INV-', max_length=80, null=True)),
                ('name', models.CharField(blank=True, max_length=80, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rin', models.CharField(max_length=80)),
                ('companyTradeName', models.CharField(max_length=80)),
                ('branchCode', models.CharField(blank=True, default=0, max_length=80, null=True)),
                ('country', models.CharField(blank=True, max_length=80, null=True)),
                ('governate', models.CharField(blank=True, max_length=80, null=True)),
                ('regionCity', models.CharField(blank=True, max_length=80, null=True)),
                ('street', models.CharField(blank=True, max_length=80, null=True)),
                ('buildingNumber', models.CharField(blank=True, max_length=80, null=True)),
                ('postalCode', models.CharField(blank=True, max_length=80, null=True)),
                ('floor', models.CharField(blank=True, max_length=80, null=True)),
                ('room', models.CharField(blank=True, max_length=80, null=True)),
                ('landmark', models.CharField(blank=True, max_length=80, null=True)),
                ('additionalInformation', models.CharField(blank=True, max_length=80, null=True)),
                ('deviceSerialNumber', models.CharField(blank=True, max_length=80, null=True)),
                ('syndicateLicenseNumber', models.CharField(blank=True, max_length=80, null=True)),
                ('activityCode', models.CharField(blank=True, max_length=80, null=True)),
                ('current_s', models.BooleanField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='taxableItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(blank=True, max_length=10, null=True)),
                ('rate', models.FloatField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='taxTotals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taxType', models.CharField(blank=True, max_length=80, null=True)),
                ('amount', models.FloatField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaxTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Code', models.CharField(blank=True, max_length=80, null=True)),
                ('Desc_en', models.CharField(blank=True, max_length=80, null=True)),
                ('Desc_ar', models.CharField(blank=True, max_length=80, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaxTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
                ('taxes', models.ManyToManyField(to='ereciept.taxableItems')),
            ],
        ),
        migrations.CreateModel(
            name='TaxSubtypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Code', models.CharField(blank=True, max_length=80, null=True)),
                ('Desc_en', models.CharField(blank=True, max_length=80, null=True)),
                ('Desc_ar', models.CharField(blank=True, max_length=80, null=True)),
                ('TaxtypeReference', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ereciept.taxtypes')),
            ],
        ),
        migrations.AddField(
            model_name='taxableitems',
            name='subType',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ereciept.taxsubtypes'),
        ),
        migrations.AddField(
            model_name='taxableitems',
            name='taxType',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ereciept.taxtypes'),
        ),
        migrations.CreateModel(
            name='Receiept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postingdate', models.DateTimeField(blank=True, null=True)),
                ('dateTimeIssued', models.CharField(blank=True, max_length=80, null=True)),
                ('receiptNumber', models.CharField(blank=True, max_length=80, null=True)),
                ('uuid', models.CharField(blank=True, max_length=80, null=True)),
                ('previousUUID', models.CharField(blank=True, max_length=80, null=True)),
                ('referenceOldUUID', models.CharField(blank=True, max_length=80, null=True)),
                ('currency', models.CharField(blank=True, choices=[('AED', 'UAE Dirham'), ('AFN', 'Afghani'), ('ALL', 'Lek'), ('AMD', 'Armenian Dram'), ('ANG', 'Netherlands Antillean Guilder'), ('AOA', 'Kwanza'), ('ARS', 'Argentine Peso'), ('AUD', 'Australian Dollar'), ('AWG', 'Aruban Florin'), ('AZN', 'Azerbaijan Manat'), ('BAM', 'Convertible Mark'), ('BBD', 'Barbados Dollar'), ('BDT', 'Taka'), ('BGN', 'Bulgarian Lev'), ('BHD', 'Bahraini Dinar'), ('BIF', 'Burundi Franc'), ('BMD', 'Bermudian Dollar'), ('BND', 'Brunei Dollar'), ('BOB', 'Boliviano'), ('BOV', 'Mvdol'), ('BRL', 'Brazilian Real'), ('BSD', 'Bahamian Dollar'), ('BTN', 'Ngultrum'), ('BWP', 'Pula'), ('BYN', 'Belarusian Ruble'), ('BZD', 'Belize Dollar'), ('CAD', 'Canadian Dollar'), ('CDF', 'Congolese Franc'), ('CHE', 'WIR Euro'), ('CHF', 'Swiss Franc'), ('CHW', 'WIR Franc'), ('CLF', 'Unidad de Fomento'), ('CLP', 'Chilean Peso'), ('CNY', 'Yuan Renminbi'), ('COP', 'Colombian Peso'), ('COU', 'Unidad de Valor Real'), ('CRC', 'Costa Rican Colon'), ('CUC', 'Peso Convertible'), ('CUP', 'Cuban Peso'), ('CVE', 'Cabo Verde Escudo'), ('CZK', 'Czech Koruna'), ('DJF', 'Djibouti Franc'), ('DKK', 'Danish Krone'), ('DOP', 'Dominican Peso'), ('DZD', 'Algerian Dinar'), ('EGP', 'Egyptian Pound'), ('ERN', 'Nakfa'), ('ETB', 'Ethiopian Birr'), ('EUR', 'Euro'), ('FJD', 'Fiji Dollar'), ('FKP', 'Falkland Islands Pound'), ('GBP', 'Pound Sterling'), ('GEL', 'Lari'), ('GHS', 'Ghana Cedi'), ('GIP', 'Gibraltar Pound'), ('GMD', 'Dalasi'), ('GNF', 'Guinean Franc'), ('GTQ', 'Quetzal'), ('GYD', 'Guyana Dollar'), ('HKD', 'Hong Kong Dollar'), ('HNL', 'Lempira'), ('HRK', 'Kuna'), ('HTG', 'Gourde'), ('HUF', 'Forint'), ('IDR', 'Rupiah'), ('ILS', 'New Israeli Sheqel'), ('INR', 'Indian Rupee'), ('IQD', 'Iraqi Dinar'), ('IRR', 'Iranian Rial'), ('ISK', 'Iceland Krona'), ('JMD', 'Jamaican Dollar'), ('JOD', 'Jordanian Dinar'), ('JPY', 'Yen'), ('KES', 'Kenyan Shilling'), ('KGS', 'Som'), ('KHR', 'Riel'), ('KMF', 'Comorian Franc '), ('KPW', 'North Korean Won'), ('KRW', 'Won'), ('KWD', 'Kuwaiti Dinar'), ('KYD', 'Cayman Islands Dollar'), ('KZT', 'Tenge'), ('LAK', 'Lao Kip'), ('LBP', 'Lebanese Pound'), ('LKR', 'Sri Lanka Rupee'), ('LRD', 'Liberian Dollar'), ('LSL', 'Loti'), ('LYD', 'Libyan Dinar'), ('MAD', 'Moroccan Dirham'), ('MDL', 'Moldovan Leu'), ('MGA', 'Malagasy Ariary'), ('MKD', 'Denar'), ('MMK', 'Kyat'), ('MNT', 'Tugrik'), ('MOP', 'Pataca'), ('MRU', 'Ouguiya'), ('MUR', 'Mauritius Rupee'), ('MVR', 'Rufiyaa'), ('MWK', 'Malawi Kwacha'), ('MXN', 'Mexican Peso'), ('MXV', 'Mexican Unidad de Inversion (UDI)'), ('MYR', 'Malaysian Ringgit'), ('MZN', 'Mozambique Metical'), ('NAD', 'Namibia Dollar'), ('NGN', 'Naira'), ('NIO', 'Cordoba Oro'), ('NOK', 'Norwegian Krone'), ('NPR', 'Nepalese Rupee'), ('NZD', 'New Zealand Dollar'), ('OMR', 'Rial Omani'), ('PAB', 'Balboa'), ('PEN', 'Sol'), ('PGK', 'Kina'), ('PHP', 'Philippine Peso'), ('PKR', 'Pakistan Rupee'), ('PLN', 'Zloty'), ('PYG', 'Guarani'), ('QAR', 'Qatari Rial'), ('RON', 'Romanian Leu'), ('RSD', 'Serbian Dinar'), ('RUB', 'Russian Ruble'), ('RWF', 'Rwanda Franc'), ('SAR', 'Saudi Riyal'), ('SBD', 'Solomon Islands Dollar'), ('SCR', 'Seychelles Rupee'), ('SDG', 'Sudanese Pound'), ('SEK', 'Swedish Krona'), ('SGD', 'Singapore Dollar'), ('SHP', 'Saint Helena Pound'), ('SLL', 'Leone'), ('SOS', 'Somali Shilling'), ('SRD', 'Surinam Dollar'), ('SSP', 'South Sudanese Pound'), ('STN', 'Dobra'), ('SVC', 'El Salvador Colon'), ('SYP', 'Syrian Pound'), ('SZL', 'Lilangeni'), ('THB', 'Baht'), ('TJS', 'Somoni'), ('TMT', 'Turkmenistan New Manat'), ('TND', 'Tunisian Dinar'), ('TOP', 'Pa’anga'), ('TRY', 'Turkish Lira'), ('TTD', 'Trinidad and Tobago Dollar'), ('TWD', 'New Taiwan Dollar'), ('TZS', 'Tanzanian Shilling'), ('UAH', 'Hryvnia'), ('UGX', 'Uganda Shilling'), ('USD', 'US Dollar'), ('USN', 'US Dollar (Next day)'), ('UYI', 'Uruguay Peso en Unidades Indexadas (UI)'), ('UYU', 'Peso Uruguayo'), ('UYW', 'Unidad Previsional'), ('UZS', 'Uzbekistan Sum'), ('VED', 'Bolívar Soberano'), ('VES', 'Bolívar Soberano'), ('VND', 'Dong'), ('VUV', 'Vatu'), ('WST', 'Tala'), ('XAF', 'CFA Franc BEAC'), ('XAG', 'Silver'), ('XAU', 'Gold'), ('XBA', 'Bond Markets Unit European Composite Unit (EURCO)'), ('XBB', 'Bond Markets Unit European Monetary Unit (E.M.U.-6)'), ('XBC', 'Bond Markets Unit European Unit of Account 9 (E.U.A.-9)'), ('XBD', 'Bond Markets Unit European Unit of Account 17 (E.U.A.-17)'), ('XCD', 'East Caribbean Dollar'), ('XDR', 'SDR (Special Drawing Right)'), ('XOF', 'CFA Franc BCEAO'), ('XPD', 'Palladium'), ('XPF', 'CFP Franc'), ('XPT', 'Platinum'), ('XSU', 'Sucre'), ('XTS', 'Codes specifically reserved for testing purposes'), ('XUA', 'ADB Unit of Account'), ('XXX', 'The codes assigned for transactions where no currency is involved'), ('YER', 'Yemeni Rial'), ('ZAR', 'Rand'), ('ZMW', 'Zambian Kwacha'), ('ZWL', 'Zimbabwe Dollar')], default='EGP', max_length=80, null=True)),
                ('exchangeRate', models.FloatField(blank=True, default=1, max_length=10, null=True)),
                ('sOrderNameCode', models.CharField(blank=True, max_length=80, null=True)),
                ('orderdeliveryMode', models.CharField(blank=True, choices=[('FC', 'From the company place'), ('TO', 'Transport by others'), ('TC', 'Transported by the company')], default='FC', max_length=80, null=True)),
                ('grossWeight', models.FloatField(blank=True, max_length=10, null=True)),
                ('netWeight', models.FloatField(blank=True, max_length=10, null=True)),
                ('receiptType', models.CharField(blank=True, default='s', max_length=80, null=True)),
                ('typeVersion', models.CharField(blank=True, default='1.2', max_length=80, null=True)),
                ('buyer_type', models.CharField(blank=True, choices=[('P', 'Person'), ('B', 'Business'), ('F', 'Foreigner')], default='P', max_length=80, null=True)),
                ('buyer_id', models.CharField(blank=True, max_length=80, null=True)),
                ('buyer_name', models.CharField(blank=True, max_length=80, null=True)),
                ('buyer_mobileNumber', models.CharField(blank=True, max_length=80, null=True)),
                ('buyer_paymentNumber', models.CharField(blank=True, max_length=80, null=True)),
                ('totalSales', models.FloatField(blank=True, default=0, max_length=10, null=True)),
                ('totalCommercialDiscount', models.FloatField(blank=True, default=0, max_length=10, null=True)),
                ('totalItemsDiscount', models.FloatField(blank=True, default=0, max_length=10, null=True)),
                ('netAmount', models.FloatField(blank=True, default=0, max_length=10, null=True)),
                ('feesAmount', models.FloatField(blank=True, default=0, max_length=10, null=True)),
                ('totalAmount', models.FloatField(blank=True, default=0, max_length=10, null=True)),
                ('paymentMethod', models.CharField(blank=True, max_length=80, null=True)),
                ('adjustment', models.FloatField(blank=True, default=0, max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('docstatus', models.CharField(blank=True, default='-1', max_length=80, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('extraReceiptDiscountData', models.ManyToManyField(blank=True, null=True, to='ereciept.DiscountObj')),
                ('itemData', models.ManyToManyField(blank=True, null=True, to='ereciept.itemData')),
                ('seller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ereciept.seller')),
                ('serial_number', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ereciept.receieptserial')),
                ('taxTotals', models.ManyToManyField(blank=True, null=True, to='ereciept.taxTotals')),
            ],
        ),
        migrations.AddField(
            model_name='itemdata',
            name='taxableItems',
            field=models.ManyToManyField(blank=True, null=True, to='ereciept.taxableItems'),
        ),
        migrations.AddField(
            model_name='itemdata',
            name='taxtemplate',
            field=models.ManyToManyField(blank=True, to='ereciept.TaxTemplate'),
        ),
    ]
