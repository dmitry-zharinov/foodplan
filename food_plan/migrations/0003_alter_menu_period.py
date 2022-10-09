# Generated by Django 4.1.2 on 2022-10-06 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_plan', '0002_alter_menu_options_remove_allergen_allergen_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='period',
            field=models.CharField(choices=[('3', '3 мес.'), ('12', '12 мес.')], default='3', max_length=10, verbose_name='Срок подписки'),
        ),
    ]
