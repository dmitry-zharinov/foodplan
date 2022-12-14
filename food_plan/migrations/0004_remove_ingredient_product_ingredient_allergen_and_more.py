# Generated by Django 4.1.2 on 2022-10-06 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food_plan', '0003_recipe_portions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='product',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='allergen',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='food_plan.allergen', verbose_name='Название аллергена'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True, verbose_name='Цена за штуку'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='title',
            field=models.CharField(db_index=True, default='ингредиент', max_length=120, verbose_name='Название ингредиента'),
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='Unit',
        ),
    ]
