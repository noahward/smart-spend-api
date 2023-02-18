# Generated by Django 4.1.7 on 2023-02-17 02:59

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0002_account_kind"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="account",
            name="unique_account",
        ),
        migrations.RenameField(
            model_name="account",
            old_name="user_id",
            new_name="user",
        ),
        migrations.AddConstraint(
            model_name="account",
            constraint=models.UniqueConstraint(
                fields=("name", "user"), name="unique_account"
            ),
        ),
    ]