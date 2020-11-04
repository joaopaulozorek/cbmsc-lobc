# Generated by Django 3.1.2 on 2020-11-04 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcs', '0004_auto_20201020_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='bc',
            name='bc_bcp',
            field=models.BooleanField(default=False, verbose_name='Bombeiro Civil Profissional:'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='usu_escolaridade',
            field=models.IntegerField(choices=[(0, 'Ensino Fundamental Incompleto'), (1, 'Ensino Fundamental Completo'), (2, 'Ensino Médio Incompleto'), (3, 'Ensino Médio Completo'), (4, 'Ensino Superior Incompleto'), (5, 'Ensino Superior Completo'), (6, 'Não Informado')], default=6, verbose_name='Escolaridade:'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='usu_estado_civil',
            field=models.IntegerField(choices=[(0, 'Solteiro (a)'), (1, 'Casado (a)'), (2, 'Divorciado (a)'), (3, 'Separado (a)'), (4, 'Viúvo (a)'), (5, 'Outro'), (6, 'Não Informado')], default=6, verbose_name='Estado civil:'),
        ),
    ]
