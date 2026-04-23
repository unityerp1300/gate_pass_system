from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material_pass', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialgatepass',
            name='consignor_office_address',
            field=models.TextField(blank=True, default='', verbose_name='Office Address'),
        ),
        migrations.AddField(
            model_name='materialgatepass',
            name='bank_name',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Bank Name'),
        ),
        migrations.AddField(
            model_name='materialgatepass',
            name='bank_account_number',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Account Number'),
        ),
        migrations.AddField(
            model_name='materialgatepass',
            name='bank_ifsc',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='IFSC Code'),
        ),
        migrations.AddField(
            model_name='materialgatepass',
            name='rounding_off',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Rounding Off'),
        ),
    ]
