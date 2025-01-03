# Generated by Django 3.2.5 on 2023-03-07 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('itemType', models.CharField(blank=True, max_length=250, null=True)),
                ('itemCode', models.CharField(blank=True, max_length=250, null=True)),
                ('unitType', models.CharField(blank=True, choices=[('2Z', 'Millivolt ( mV )'), ('4K', 'Milliampere ( mA )'), ('4O', 'Microfarad ( microF )'), ('A87', 'Gigaohm ( GOhm )'), ('A93', 'Gram/Cubic meter ( g/m3 )'), ('A94', 'Gram/cubic centimeter ( g/cm3 )'), ('AMP', 'Ampere ( A )'), ('ANN', 'Years ( yr )'), ('B22', 'Kiloampere ( kA )'), ('B49', 'Kiloohm ( kOhm )'), ('B75', 'Megohm ( MOhm )'), ('B78', 'Megavolt ( MV )'), ('B84', 'Microampere ( microA )'), ('BAR', 'bar ( bar )'), ('BBL', 'Barrel (oil 42 gal.)'), ('BG', 'Bag ( Bag )'), ('BO', 'Bottle ( Bt. )'), ('BOX', 'Box'), ('C10', 'Millifarad ( mF )'), ('C39', 'Nanoampere ( nA )'), ('C41', 'Nanofarad ( nF )'), ('C45', 'Nanometer ( nm )'), ('C62', 'Activity unit ( AU )'), ('CA', 'Canister ( Can )'), ('CMK', 'Square centimeter ( cm2 )'), ('CMQ', 'Cubic centimeter ( cm3 )'), ('CMT', 'Centimeter ( cm )'), ('CS', 'Case ( Case )'), ('CT', 'Carton ( Car )'), ('CTL', 'Centiliter ( Cl )'), ('D10', 'Siemens per meter ( S/m )'), ('D33', 'Tesla ( D )'), ('D41', 'Ton/Cubic meter ( t/m3 )'), ('DAY', 'Days ( d )'), ('DMT', 'Decimeter ( dm )'), ('DRM', 'DRUM'), ('EA', 'each (ST) ( ST )'), ('FAR', 'Farad ( F )'), ('FOT', 'Foot ( Foot )'), ('FTK', 'Square foot ( ft2 )'), ('FTQ', 'Cubic foot ( ft3 )'), ('G42', 'Microsiemens per centimeter ( microS/cm )'), ('GL', 'Gram/liter ( g/l )'), ('GLL', 'gallon ( gal )'), ('GM', 'Gram/square meter ( g/m2 )'), ('GPT', 'Gallon per thousand'), ('GRM', 'Gram ( g )'), ('H63', 'Milligram/Square centimeter ( mg/cm2 )'), ('HHP', 'Hydraulic Horse Power'), ('HLT', 'Hectoliter ( hl )'), ('HTZ', 'Hertz (1/second) ( Hz )'), ('HUR', 'Hours ( hrs )'), ('IE', 'Number of Persons ( PRS )'), ('INH', 'Inch ( “” )'), ('INK', 'Square inch ( Inch2 )'), ('IVL', 'Interval'), ('JOB', 'JOB'), ('KGM', 'Kilogram ( KG )'), ('KHZ', 'Kilohertz ( kHz )'), ('KMH', 'Kilometer/hour ( km/h )'), ('KMK', 'Square kilometer ( km2 )'), ('KMQ', 'Kilogram/cubic meter ( kg/m3 )'), ('KMT', 'Kilometer ( km )'), ('KSM', 'Kilogram/Square meter ( kg/m2 )'), ('KVT', 'Kilovolt ( kV )'), ('KWT', 'Kilowatt ( KW )'), ('LB', 'pounds '), ('LTR', 'Liter ( l )'), ('LVL', 'Level'), ('M', 'Meter ( m )'), ('MAN', 'Man'), ('MAW', 'Megawatt ( VA )'), ('MGM', 'Milligram ( mg )'), ('MHZ', 'Megahertz ( MHz )'), ('MIN', 'Minute ( min )'), ('MMK', 'Square millimeter ( mm2 )'), ('MMQ', 'Cubic millimeter ( mm3 )'), ('MMT', 'Millimeter ( mm )'), ('MON', 'Months ( Months )'), ('MTK', 'Square meter ( m2 )'), ('MTQ', 'Cubic meter ( m3 )'), ('OHM', 'Ohm ( Ohm )'), ('ONZ', 'Ounce ( oz )'), ('PAL', 'Pascal ( Pa )'), ('PF', 'Pallet ( PAL )'), ('PK', 'Pack ( PAK )'), ('PMP', 'pump'), ('RUN', 'run'), ('SH', 'Shrink ( Shrink )'), ('SK', 'Sack'), ('SMI', 'Mile ( mile )'), ('ST', 'Ton (short,2000 lb)'), ('TNE', 'Tonne ( t )'), ('TON', 'Ton (metric)'), ('VLT', 'Volt ( V )'), ('WEE', 'Weeks ( Weeks )'), ('WTT', 'Watt ( W )'), ('X03', 'Meter/Hour ( m/h )'), ('YDQ', 'Cubic yard ( yd3 )'), ('YRD', 'Yards ( yd )')], max_length=250, null=True)),
                ('internalCode', models.CharField(blank=True, max_length=250, null=True)),
                ('unitValue_currencySold', models.CharField(default='EGP', max_length=250)),
                ('unitValue_amountEGP', models.DecimalField(blank=True, decimal_places=5, max_digits=100, null=True)),
            ],
        ),
    ]
