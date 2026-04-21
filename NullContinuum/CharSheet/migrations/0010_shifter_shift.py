from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CharSheet', '0009_nl_strain_and_feat_frame'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShifterShift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Nome do Shift')),
                ('transform_strain', models.PositiveIntegerField(default=0, verbose_name='Custo de Transformação (Strain)')),
                ('transform_ap', models.PositiveIntegerField(default=0, verbose_name='Custo de Transformação (AP)')),
                ('character', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='shifter_shift',
                    to='CharSheet.character',
                )),
            ],
        ),
        migrations.CreateModel(
            name='ShiftPassive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('order', models.PositiveIntegerField(default=0)),
                ('shift', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='passives',
                    to='CharSheet.shiftershift',
                )),
            ],
            options={'ordering': ['order']},
        ),
        migrations.CreateModel(
            name='ShiftActive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Nome')),
                ('damage_effect', models.CharField(max_length=300, verbose_name='Dano / Efeito')),
                ('range_hexes', models.PositiveIntegerField(default=1, verbose_name='Alcance (hexes)')),
                ('strain_cost', models.PositiveIntegerField(default=0, verbose_name='Custo em Strain')),
                ('duration', models.CharField(max_length=120, verbose_name='Duração')),
                ('order', models.PositiveIntegerField(default=0)),
                ('shift', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='actives',
                    to='CharSheet.shiftershift',
                )),
            ],
            options={'ordering': ['order']},
        ),
        migrations.CreateModel(
            name='ShiftCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('order', models.PositiveIntegerField(default=0)),
                ('shift', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='costs',
                    to='CharSheet.shiftershift',
                )),
            ],
            options={'ordering': ['order']},
        ),
    ]
