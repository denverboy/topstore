# Generated by Django 4.2.3 on 2023-07-27 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_specificationname'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecificationValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
            ],
        ),
    ]
