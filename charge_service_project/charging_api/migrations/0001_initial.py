# Generated by Django 5.1.7 on 2025-03-15 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChargingRequestLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_id', models.CharField(max_length=36)),
                ('driver_token', models.CharField(max_length=80)),
                ('callback_url', models.URLField()),
                ('request_time', models.DateTimeField(auto_now_add=True)),
                ('decision_time', models.DateTimeField(blank=True, null=True)),
                ('decision', models.CharField(choices=[('allowed', 'Allowed'), ('not_allowed', 'Not Allowed'), ('unknown', 'Unknown'), ('invalid', 'Invalid')], default='unknown', max_length=20)),
            ],
        ),
    ]
