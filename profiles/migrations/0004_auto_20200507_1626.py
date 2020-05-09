# Generated by Django 3.0.5 on 2020-05-07 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_memberships_post_subscription_usermembership'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberships',
            name='Membership_type',
            field=models.CharField(choices=[('Free', 'free'), ('Monthly', 'month'), ('Yearly', 'year')], default='free', max_length=40),
        ),
        migrations.AlterField(
            model_name='usermembership',
            name='membership',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Memberships'),
        ),
    ]
