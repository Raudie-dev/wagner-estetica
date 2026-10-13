from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0006_appointment_notas'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=60, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('orden', models.IntegerField(default=10)),
            ],
            options={
                'ordering': ['orden', 'id'],
            },
        ),
        migrations.AddField(
            model_name='service',
            name='categoria',
            field=models.CharField(
                blank=True,
                default='dermocosmiatria',
                max_length=60,
                null=True,
            ),
        ),
    ]
