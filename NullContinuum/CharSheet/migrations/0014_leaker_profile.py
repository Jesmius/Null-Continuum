from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CharSheet', '0013_maker_construct_stats'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LeakerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='leaker_profile',
                    to='CharSheet.character',
                )),
            ],
        ),
        migrations.CreateModel(
            name='LeakerEmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Nome')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('radius', models.PositiveIntegerField(
                    blank=True, null=True,
                    help_text='Deixe em branco se o efeito é apenas sobre si mesmo',
                    verbose_name='Raio (hexes)',
                )),
                ('order', models.PositiveIntegerField(default=0)),
                ('profile', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='emissions',
                    to='CharSheet.leakerprofile',
                )),
            ],
            options={'ordering': ['order']},
        ),
        migrations.CreateModel(
            name='LeakerVolatility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage_label', models.CharField(max_length=40, verbose_name='Estágio')),
                ('description', models.TextField(verbose_name='Efeitos neste estágio')),
                ('order', models.PositiveIntegerField(default=0)),
                ('profile', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='volatility_stages',
                    to='CharSheet.leakerprofile',
                )),
            ],
            options={'ordering': ['order']},
        ),
        migrations.CreateModel(
            name='LeakerBleed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Nome')),
                ('effect', models.CharField(max_length=300, verbose_name='Dano / Efeito')),
                ('ap_cost', models.PositiveIntegerField(default=1, verbose_name='Custo em AP')),
                ('strain_info', models.CharField(blank=True, max_length=120, verbose_name='Info de Strain')),
                ('description', models.TextField(blank=True, verbose_name='Notas adicionais')),
                ('order', models.PositiveIntegerField(default=0)),
                ('profile', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='bleeds',
                    to='CharSheet.leakerprofile',
                )),
            ],
            options={'ordering': ['order']},
        ),
    ]
