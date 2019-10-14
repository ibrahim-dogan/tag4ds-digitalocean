# Generated by Django 2.2.4 on 2019-08-25 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fileupload', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jsonfile',
            name='name',
            field=models.CharField(default='uploaded_file', max_length=100),
        ),
        migrations.AddField(
            model_name='jsonfile',
            name='tags_added',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='UnprocessedRow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json_row', models.TextField()),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fileupload.JsonFile')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=100)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fileupload.JsonFile')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessedRow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json_row', models.TextField()),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fileupload.JsonFile')),
            ],
        ),
    ]