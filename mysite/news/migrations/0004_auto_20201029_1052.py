# Generated by Django 3.1.2 on 2020-10-29 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20201017_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='news.category', verbose_name='Категория'),
            preserve_default=False,
        ),
    ]