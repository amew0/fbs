# Generated by Django 4.1.6 on 2023-03-10 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0008_alter_creditcarddetail_linked_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='Debit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DebitName', models.CharField(max_length=25)),
                ('DebitFinalDate', models.TextField(blank=True, null=True)),
                ('DebitAmount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('DebitInstallmentMonthly', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('accountNumDebit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accountNumDebit', to='banking.creditcarddetail')),
            ],
        ),
    ]