# Generated by Django 4.1.7 on 2023-03-04 12:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0005_remove_allowance_userb_allowance_usermain_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditcarddetail',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='creditcarddetail',
            name='linked_users',
            field=models.ManyToManyField(null=True, related_name='linked_accounts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='allowance',
            name='allowance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.DeleteModel(
            name='Balance',
        ),
    ]
