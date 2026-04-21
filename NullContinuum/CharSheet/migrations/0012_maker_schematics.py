from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CharSheet', '0011_changer_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='MakerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='maker_profile',
                    to='CharSheet.character',
                )),
            ],
        ),
        migrations.CreateModel(
            name='MakerSchematic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Nome do Schematic')),
                ('construction_type', models.CharField(
                    choices=[('STRUCTURE','Structure'),('EQUIPMENT','Equipment'),('CONSTRUCT','Construct'),('ZONE','Zone')],
                    max_length=12, verbose_name='Tipo',
                )),
                ('extra_strain', models.PositiveIntegerField(default=0, verbose_name='Strain Extra (design)')),
                ('stability', models.PositiveIntegerField(
                    default=0,
                    validators=[django.core.validators.MaxValueValidator(3)],
                    verbose_name='Stability',
                )),
                ('notes', models.TextField(blank=True, verbose_name='Notas')),
                ('order', models.PositiveIntegerField(default=0)),
                ('cover_description', models.TextField(blank=True, verbose_name='Cover')),
                ('damage_description', models.TextField(blank=True, verbose_name='Damage')),
                ('equipment_category', models.CharField(
                    blank=True,
                    choices=[('WEAPON','Weapon'),('ARMOUR','Armour'),('CONSUMABLE','Consumable'),('NL_ENHANCEMENT','NL Enhancement')],
                    max_length=20, verbose_name='Categoria',
                )),
                ('equipment_tier', models.PositiveIntegerField(
                    default=1,
                    validators=[django.core.validators.MaxValueValidator(3)],
                    verbose_name='Tier',
                )),
                ('equipment_description', models.TextField(blank=True, verbose_name='Descrição do Equipment')),
                ('nl_enhancement_description', models.TextField(blank=True, verbose_name='NL Enhancement')),
                ('body_tier', models.PositiveIntegerField(
                    default=1,
                    validators=[django.core.validators.MaxValueValidator(3)],
                    verbose_name='Body Tier',
                )),
                ('body_description', models.TextField(blank=True, verbose_name='Body Description')),
                ('area_tier', models.PositiveIntegerField(
                    default=1,
                    validators=[django.core.validators.MaxValueValidator(3)],
                    verbose_name='Area Tier',
                )),
                ('zone_area_description', models.TextField(blank=True, verbose_name='Área Description')),
                ('profile', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='schematics',
                    to='CharSheet.makerprofile',
                )),
            ],
            options={'ordering': ['order']},
        ),
        migrations.CreateModel(
            name='ConstructPassive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('order', models.PositiveIntegerField(default=0)),
                ('schematic', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='construct_passives',
                    to='CharSheet.makerschematic',
                )),
            ],
            options={'ordering': ['order']},
        ),
        migrations.CreateModel(
            name='ConstructActive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('order', models.PositiveIntegerField(default=0)),
                ('schematic', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='construct_actives',
                    to='CharSheet.makerschematic',
                )),
            ],
            options={'ordering': ['order']},
        ),
        migrations.CreateModel(
            name='ZoneEffect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('order', models.PositiveIntegerField(default=0)),
                ('schematic', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='zone_effects',
                    to='CharSheet.makerschematic',
                )),
            ],
            options={'ordering': ['order']},
        ),
    ]
