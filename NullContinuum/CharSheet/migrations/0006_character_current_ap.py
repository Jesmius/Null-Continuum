from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CharSheet', '0005_traitdefinition_charactertrait'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='current_ap',
            field=models.IntegerField(default=3, verbose_name='AP Atual'),
        ),
    ]
