# Generated by Django 4.0 on 2022-01-16 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basketproduct',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.customer', verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='orders',
            field=models.ManyToManyField(null=True, related_name='related_custoomer', to='app.Order'),
        ),
    ]
