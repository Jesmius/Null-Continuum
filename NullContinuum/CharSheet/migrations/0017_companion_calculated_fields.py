from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CharSheet', '0016_companions'),
    ]

    operations = [
        migrations.RemoveField(model_name='companionitem', name='nl_rank'),
        migrations.RemoveField(model_name='companionitem', name='max_hp'),
        migrations.RemoveField(model_name='companionitem', name='physical_defense'),
        migrations.AddField(
            model_name='companionitem',
            name='hp_bonus',
            field=models.IntegerField(default=0, verbose_name='Bônus de HP'),
        ),
        migrations.AddField(
            model_name='companionitem',
            name='pd_bonus',
            field=models.IntegerField(default=0, verbose_name='Bônus de PD (armadura/coleira/rig)'),
        ),
        migrations.AddField(
            model_name='companionitem',
            name='strain_bonus',
            field=models.IntegerField(default=0, verbose_name='Bônus de Strain'),
        ),
    ]
