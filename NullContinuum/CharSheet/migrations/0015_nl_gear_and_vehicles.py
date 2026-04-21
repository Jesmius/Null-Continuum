from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CharSheet', '0014_leaker_profile'),
    ]

    operations = [
        # ── WeaponItem NL fields ──
        migrations.AddField(model_name='weaponitem', name='is_nl',
            field=models.BooleanField(default=False, verbose_name='Não-Linear')),
        migrations.AddField(model_name='weaponitem', name='nl_constant',
            field=models.CharField(blank=True, max_length=200, verbose_name='Continuity Constant')),
        migrations.AddField(model_name='weaponitem', name='nl_passive',
            field=models.TextField(blank=True, verbose_name='Passive Expressions')),
        migrations.AddField(model_name='weaponitem', name='nl_active',
            field=models.TextField(blank=True, verbose_name='Active Expressions')),
        migrations.AddField(model_name='weaponitem', name='nl_condition_rules',
            field=models.TextField(blank=True, verbose_name='Condition Rules')),

        # ── VestmentItem NL fields ──
        migrations.AddField(model_name='vestmentitem', name='is_nl',
            field=models.BooleanField(default=False, verbose_name='Não-Linear')),
        migrations.AddField(model_name='vestmentitem', name='nl_constant',
            field=models.CharField(blank=True, max_length=200, verbose_name='Continuity Constant')),
        migrations.AddField(model_name='vestmentitem', name='nl_passive',
            field=models.TextField(blank=True, verbose_name='Passive Expressions')),
        migrations.AddField(model_name='vestmentitem', name='nl_active',
            field=models.TextField(blank=True, verbose_name='Active Expressions')),
        migrations.AddField(model_name='vestmentitem', name='nl_condition_rules',
            field=models.TextField(blank=True, verbose_name='Condition Rules')),

        # ── ConsumableItem NL fields ──
        migrations.AddField(model_name='consumableitem', name='is_nl',
            field=models.BooleanField(default=False, verbose_name='Não-Linear')),
        migrations.AddField(model_name='consumableitem', name='nl_constant',
            field=models.CharField(blank=True, max_length=200, verbose_name='Continuity Constant')),
        migrations.AddField(model_name='consumableitem', name='nl_passive',
            field=models.TextField(blank=True, verbose_name='Passive Expressions')),
        migrations.AddField(model_name='consumableitem', name='nl_active',
            field=models.TextField(blank=True, verbose_name='Active Expressions')),
        migrations.AddField(model_name='consumableitem', name='nl_condition_rules',
            field=models.TextField(blank=True, verbose_name='Condition Rules')),

        # ── VehicleItem ──
        migrations.CreateModel(
            name='VehicleItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                       serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Nome')),
                ('size_tier', models.CharField(
                    choices=[('BIKE', 'Bike'), ('LIGHT', 'Light'), ('MEDIUM', 'Medium'),
                             ('HEAVY', 'Heavy'), ('MASSIVE', 'Massive')],
                    default='LIGHT', max_length=10, verbose_name='Size Tier')),
                ('current_hp', models.IntegerField(default=0, verbose_name='HP Atual')),
                ('max_hp', models.PositiveIntegerField(default=1, verbose_name='HP Máximo')),
                ('armor_value', models.IntegerField(default=0, verbose_name='Armor Value')),
                ('speed', models.IntegerField(default=0, verbose_name='Speed')),
                ('handling', models.IntegerField(default=0, verbose_name='Handling')),
                ('seats', models.PositiveIntegerField(default=1, verbose_name='Assentos')),
                ('cargo_slots', models.PositiveIntegerField(default=0, verbose_name='Cargo Slots')),
                ('fuel_type', models.CharField(blank=True, max_length=80,
                              verbose_name='Tipo de Combustível')),
                ('fuel_range', models.CharField(blank=True, max_length=80,
                               verbose_name='Alcance (combustível)')),
                ('traits', models.TextField(blank=True, verbose_name='Traits')),
                ('is_nl', models.BooleanField(default=False, verbose_name='Não-Linear')),
                ('nl_constant', models.CharField(blank=True, max_length=200,
                                verbose_name='Continuity Constant')),
                ('nl_passive', models.TextField(blank=True, verbose_name='Passive Expressions')),
                ('nl_active', models.TextField(blank=True, verbose_name='Active Expressions')),
                ('nl_condition_rules', models.TextField(blank=True, verbose_name='Condition Rules')),
                ('character', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='vehicles', to='CharSheet.character')),
            ],
            options={
                'verbose_name': 'Veículo',
                'verbose_name_plural': 'Veículos',
                'ordering': ['name'],
            },
        ),
    ]
