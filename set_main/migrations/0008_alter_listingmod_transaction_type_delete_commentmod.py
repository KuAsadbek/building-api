# Generated by Django 5.2.3 on 2025-07-17 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('set_main', '0007_alter_listingmod_transaction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listingmod',
            name='transaction_type',
            field=models.CharField(blank=True, choices=[('sale', 'Продажа'), ('rent', 'Аренда')], max_length=50, null=True),
        ),
        migrations.DeleteModel(
            name='CommentMod',
        ),
    ]
