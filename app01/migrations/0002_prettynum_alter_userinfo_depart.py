# Generated by Django 4.2.4 on 2023-08-19 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PrettyNum",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("mobile", models.CharField(max_length=11, verbose_name="手机号")),
                ("price", models.IntegerField(default=0, verbose_name="价格")),
                (
                    "level",
                    models.SmallIntegerField(
                        choices=[(1, "senior"), (2, "medium"), (3, "primary")],
                        verbose_name="等级",
                    ),
                ),
                (
                    "status",
                    models.SmallIntegerField(
                        choices=[(1, "occupied"), (2, "empty")],
                        default=2,
                        verbose_name="状态",
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="depart",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="app01.department",
                verbose_name="所属部门",
            ),
            preserve_default=False,
        ),
    ]
