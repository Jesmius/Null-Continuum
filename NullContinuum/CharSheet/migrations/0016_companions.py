from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CharSheet', '0015_nl_gear_and_vehicles'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Nome')),
                ('species', models.CharField(blank=True, max_length=120, verbose_name='Espécie / Tipo')),
                ('agility', models.PositiveIntegerField(default=1, verbose_name='AGI')),
                ('fortitude', models.PositiveIntegerField(default=1, verbose_name='FOR')),
                ('insight', models.PositiveIntegerField(default=1, verbose_name='INS')),
                ('presence', models.PositiveIntegerField(default=1, verbose_name='PRE')),
                ('stability', models.PositiveIntegerField(default=1, verbose_name='STA')),
                ('current_hp', models.IntegerField(default=0, verbose_name='HP Atual')),
                ('max_hp', models.PositiveIntegerField(default=1, verbose_name='HP Máximo')),
                ('physical_defense', models.IntegerField(default=10, verbose_name='PD')),
                ('nl_rank', models.PositiveIntegerField(default=0, verbose_name='NLC')),
                ('bond_rating', models.PositiveIntegerField(default=1, verbose_name='Bond Rating')),
                ('current_strain', models.PositiveIntegerField(default=0, verbose_name='Strain Atual')),
                ('attack', models.CharField(blank=True, max_length=200, verbose_name='Ataque Base')),
                ('skills', models.TextField(blank=True, verbose_name='Skills')),
                ('traits', models.TextField(blank=True, verbose_name='Traits')),
                ('is_nl', models.BooleanField(default=False, verbose_name='Não-Linear')),
                ('nl_constant', models.CharField(blank=True, max_length=200, verbose_name='Continuity Constant')),
                ('nl_passive', models.TextField(blank=True, verbose_name='Passive Expressions')),
                ('nl_active', models.TextField(blank=True, verbose_name='Active Expressions')),
                ('nl_condition_rules', models.TextField(blank=True, verbose_name='Regras de Bond / Condição')),
                ('character', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='companions',
                    to='CharSheet.character',
                )),
            ],
            options={
                'verbose_name': 'Companheiro',
                'verbose_name_plural': 'Companheiros',
                'ordering': ['name'],
            },
        ),
    ]
