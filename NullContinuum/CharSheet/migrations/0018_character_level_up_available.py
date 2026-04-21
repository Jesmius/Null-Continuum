from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CharSheet', '0017_companion_calculated_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='level_up_available',
            field=models.BooleanField(default=False, verbose_name='Level Up Disponível'),
        ),
    ]
