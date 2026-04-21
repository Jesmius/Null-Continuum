from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('CharSheet', '0017_companion_calculated_fields'),
        ('HomeApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Nome')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('gm', models.ForeignKey(
                    limit_choices_to={'role': 'GM'},
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='gm_campaigns',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'verbose_name': 'Campanha',
                'verbose_name_plural': 'Campanhas',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CampaignMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('campaign', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='memberships',
                    to='HomeApp.campaign',
                )),
                ('player', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='memberships',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'verbose_name': 'Membro',
                'verbose_name_plural': 'Membros',
                'unique_together': {('campaign', 'player')},
            },
        ),
        migrations.CreateModel(
            name='CampaignCharacter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('campaign', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='submitted_characters',
                    to='HomeApp.campaign',
                )),
                ('character', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='campaign_submissions',
                    to='CharSheet.character',
                )),
            ],
            options={
                'verbose_name': 'Personagem na Campanha',
                'verbose_name_plural': 'Personagens na Campanha',
                'unique_together': {('campaign', 'character')},
            },
        ),
    ]
