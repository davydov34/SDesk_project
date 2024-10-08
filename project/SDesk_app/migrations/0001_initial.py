# Generated by Django 5.1.1 on 2024-09-28 16:32

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dep_name', models.CharField(max_length=255, unique=True, verbose_name='Отдел')),
                ('short_name', models.CharField(blank=True, max_length=5, verbose_name='Сокращенное имя отдела')),
            ],
            options={
                'verbose_name': 'Отдел',
                'verbose_name_plural': 'Отделы',
            },
        ),
        migrations.CreateModel(
            name='PermissionLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level_name', models.CharField(max_length=30, verbose_name='Уровень доступа')),
            ],
            options={
                'verbose_name': 'Уровень доступа',
                'verbose_name_plural': 'Уровни доступа',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_code', models.CharField(max_length=5, verbose_name='Код состояния')),
                ('status_str', models.CharField(max_length=15, verbose_name='Состояние задачи')),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статусы',
            },
        ),
        migrations.CreateModel(
            name='StaffPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_name', models.CharField(max_length=100, verbose_name='Должность')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SDesk_app.department', verbose_name='Отдел')),
            ],
            options={
                'verbose_name': 'Дожность',
                'verbose_name_plural': 'Должности',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_name', models.CharField(max_length=20, unique=True, verbose_name='Имя в системе')),
                ('last_name', models.CharField(max_length=20, verbose_name='Фамилия')),
                ('first_name', models.CharField(max_length=20, verbose_name='Имя')),
                ('cell_phone', models.CharField(blank=True, max_length=16, verbose_name='Сотовый телефон')),
                ('inner_phone', models.CharField(blank=True, max_length=20, verbose_name='Внутренний номер')),
                ('super_user', models.BooleanField(default=False, verbose_name='Администратор системы SDesk')),
                ('permission_level', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='SDesk_app.permissionlevel', verbose_name='Уровень доступа')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('staff_position', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='SDesk_app.staffposition', verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_doc', models.IntegerField(default=0, verbose_name='Номер задачи')),
                ('title', models.CharField(max_length=50, verbose_name='Наименование')),
                ('description', models.TextField(blank=True, verbose_name='Комментарий к задаче')),
                ('answer', models.TextField(blank=True, verbose_name='Ответ исполнителя')),
                ('created_at', models.DateField(default=django.utils.timezone.now, editable=False)),
                ('start_exec_at', models.DateTimeField(default=None, null=True, verbose_name='Задача передана в работу в')),
                ('stop_exec_at', models.DateTimeField(default=None, null=True, verbose_name='Работа над задачей завершена в')),
                ('is_closed', models.BooleanField(default=False, verbose_name='Задача закрыта')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Задача удалена')),
                ('closing_at', models.DateTimeField(blank=True, null=True)),
                ('executor', models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Executor', to='SDesk_app.profile', verbose_name='Исполнитель')),
                ('initiator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Initiator', to='SDesk_app.profile', verbose_name='Инициатор')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SDesk_app.status', verbose_name='Статус задачи')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
    ]
