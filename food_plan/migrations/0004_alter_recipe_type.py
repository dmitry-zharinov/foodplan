# Generated by Django 4.1.2 on 2022-10-06 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_plan', '0003_alter_menu_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='type',
            field=models.CharField(choices=[('breakfast', 'завтрак'), ('lunch', 'обед'), ('supper', 'ужин'), ('dessert', 'десерт')], default='breakfast', max_length=10, verbose_name='Тип блюда'),
        ),
    ]
