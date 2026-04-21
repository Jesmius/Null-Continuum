from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CharSheet', '0010_shifter_shift'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='changer_profile',
                    to='CharSheet.character',
                )),
            ],
        ),
        migrations.CreateModel(
            name='ChangerAbility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Nome')),
                ('damage_effect', models.CharField(max_length=300, verbose_name='Dano / Efeito')),
                ('range_hexes', models.PositiveIntegerField(default=1, verbose_name='Alcance (hexes)')),
                ('strain_cost', models.PositiveIntegerField(default=0, verbose_name='Custo em Strain')),
                ('duration', models.CharField(max_length=120, verbose_name='Duração')),
                ('restrictions', models.TextField(blank=True, verbose_name='Restrictions')),
                ('order', models.PositiveIntegerField(default=0)),
                ('profile', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='abilities',
                    to='CharSheet.changerprofile',
                )),
            ],
            options={'ordering': ['order']},
        ),
    ]
