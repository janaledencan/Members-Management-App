# Generated by Django 4.1.6 on 2023-03-09 16:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0003_remove_member_date_of_adding_member_gender"),
    ]

    operations = [
        migrations.AddField(
            model_name="group",
            name="description",
            field=models.TextField(default=None, max_length=300),
        ),
        migrations.AlterField(
            model_name="member",
            name="date_of_birth",
            field=models.DateField(),
        ),
    ]
