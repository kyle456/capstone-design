# Generated by Django 2.2 on 2019-05-31 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dirview',
            fields=[
                ('recipe_menu', models.CharField(db_column='recipe_menu', max_length=50, primary_key=True, serialize=False)),
                ('dirkey', models.IntegerField()),
                ('direction', models.CharField(blank=True, max_length=170, null=True)),
                ('imgkey', models.IntegerField()),
                ('dir_image', models.CharField(blank=True, max_length=75, null=True)),
            ],
            options={
                'db_table': 'direction_image',
                'managed': False,
            },
        ),
    ]