# Generated by Django 4.1.3 on 2024-01-07 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0016_poisonous_meta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rates',
            name='baseCurrency',
        ),
        migrations.RemoveField(
            model_name='rates',
            name='foreignCurrency',
        ),
        migrations.AddField(
            model_name='rates',
            name='currency',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='rates',
            name='rate',
            field=models.DecimalField(decimal_places=5, max_digits=15),
        ),
        migrations.CreateModel(
            name='BaseCurrency',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('base_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_currency', to='apis.rates')),
            ],
        ),
    ]
