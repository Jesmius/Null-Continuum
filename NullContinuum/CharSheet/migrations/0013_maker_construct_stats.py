from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('CharSheet', '0012_maker_schematics'),
    ]

    operations = [
        migrations.AddField(
            model_name='makerschematic',
            name='use_strain',
            field=models.PositiveIntegerField(default=0, verbose_name='Custo de Uso (Strain)'),
        ),
        migrations.AddField(
            model_name='makerschematic',
            name='construct_pre',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(3)], verbose_name='PRE'),
        ),
        migrations.AddField(
            model_name='makerschematic',
            name='construct_ins',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(3)], verbose_name='INS'),
        ),
        migrations.AddField(
            model_name='makerschematic',
            name='construct_for',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(3)], verbose_name='FOR'),
        ),
        migrations.AddField(
            model_name='makerschematic',
            name='construct_agi',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(3)], verbose_name='AGI'),
        ),
        migrations.AddField(
            model_name='makerschematic',
            name='construct_current_hp',
            field=models.IntegerField(default=0, verbose_name='HP Atual do Construto'),
        ),
        migrations.RemoveField(
            model_name='makerschematic',
            name='body_description',
        ),
    ]
