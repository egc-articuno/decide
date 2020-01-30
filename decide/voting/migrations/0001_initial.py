# Generated by Django 2.0 on 2020-01-23 19:33

import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import voting.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartyCongressCandidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(blank=True, null=True)),
                ('congress_candidate', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('H', 'Hombre'), ('M', 'Mujer')], max_length=1)),
                ('postal_code', models.CharField(max_length=5, validators=[django.core.validators.RegexValidator('^[0-9]{5}$'), voting.models.PartyCongressCandidate.valid])),
            ],
        ),
        migrations.CreateModel(
            name='PartyPresidentCandidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(blank=True, null=True)),
                ('president_candidate', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('H', 'Hombre'), ('M', 'Mujer')], max_length=1)),
                ('postal_code', models.CharField(max_length=5, validators=[django.core.validators.RegexValidator('^[0-9]{5}$'), voting.models.PartyPresidentCandidate.valid])),
            ],
        ),
        migrations.CreateModel(
            name='PoliticalParty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Voting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField(blank=True, null=True)),
                ('blank_vote', models.PositiveIntegerField(default=1)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('tally', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('postproc', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('auths', models.ManyToManyField(related_name='votings', to='base.Auth')),
                ('pub_key', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='voting', to='base.Key')),
            ],
        ),
        migrations.AddField(
            model_name='politicalparty',
            name='voting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parties', to='voting.Voting'),
        ),
        migrations.AddField(
            model_name='partypresidentcandidate',
            name='politicalParty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='president_candidates', to='voting.PoliticalParty'),
        ),
        migrations.AddField(
            model_name='partycongresscandidate',
            name='politicalParty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='congress_candidates', to='voting.PoliticalParty'),
        ),
    ]