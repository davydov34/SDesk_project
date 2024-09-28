from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


# Create your models here.
class Department(models.Model):
    dep_name = models.CharField(null=False, unique=True, max_length=255, verbose_name="Отдел")
    short_name = models.CharField(blank=True, max_length=5, verbose_name="Сокращенное имя отдела")

    class Meta():
        verbose_name = "Отдел"
        verbose_name_plural = "Отделы"

    def __str__(self):
        return f'Отдел: {self.dep_name}'

class StaffPosition(models.Model):
    position_name = models.CharField(null=False, max_length=100, verbose_name="Должность")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Отдел")

    class Meta():
        verbose_name = "Дожность"
        verbose_name_plural = "Должности"

    def __str__(self):
        return f'Должность: [{self.position_name}] в отделе [{self.department.dep_name}]'

class PermissionLevel(models.Model):
    level_code = models.CharField(null=False, default='UNC', max_length=5,  verbose_name="Уровень доступа")
    level_name = models.CharField(null=False, max_length=30,  verbose_name="Уровень доступа")

    class Meta():
        verbose_name = "Уровень доступа"
        verbose_name_plural = "Уровни доступа"

    def __str__(self):
        return f'{self.level_name}'

class Status(models.Model):
    status_code = models.CharField(null=False, max_length=5, verbose_name="Код состояния")
    status_str = models.CharField(null=False, max_length=30, verbose_name="Состояние задачи")

    class Meta():
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return f'{self.status_str}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    system_name = models.CharField(null=False, unique=True, max_length=20, verbose_name="Имя в системе")
    last_name = models.CharField(null=False, max_length=20, verbose_name="Фамилия")
    first_name = models.CharField(null=False, max_length=20, verbose_name="Имя")
    staff_position = models.ForeignKey(StaffPosition, null=False, default=0, on_delete=models.CASCADE, verbose_name="Должность")
    permission_level = models.ForeignKey(PermissionLevel, null=False, default=1, on_delete=models.CASCADE, verbose_name="Уровень доступа")
    cell_phone = models.CharField(blank=True, max_length=16, verbose_name="Сотовый телефон")
    inner_phone = models.CharField(blank=True, max_length=20, verbose_name="Внутренний номер")
    super_user = models.BooleanField(default=False, verbose_name="Администратор системы SDesk")

    class Meta():
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

class Task(models.Model):
    num_doc = models.IntegerField(null=False, default=0, verbose_name="Номер задачи")
    title = models.CharField(max_length=50, null=False, verbose_name="Наименование")
    description = models.TextField(blank=True, verbose_name='Комментарий к задаче')
    answer = models.TextField(blank=True, verbose_name='Ответ исполнителя')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name="Статус задачи")
    initiator = models.ForeignKey(Profile, related_name='Initiator', on_delete=models.DO_NOTHING, verbose_name="Инициатор")
    executor = models.ForeignKey(Profile, related_name='Executor', null=True, default=0, on_delete=models.DO_NOTHING, verbose_name="Исполнитель")
    created_at = models.DateField(default=timezone.now, editable=False)
    start_exec_at = models.DateTimeField(null=True, default=None, verbose_name="Задача передана в работу в")
    stop_exec_at = models.DateTimeField(null=True, default=None, verbose_name="Работа над задачей завершена в")
    is_closed = models.BooleanField(default=False, verbose_name="Задача закрыта")
    is_deleted = models.BooleanField(default=False, verbose_name="Задача удалена")
    closing_at = models.DateTimeField(null=True, blank=True)

    class Meta():
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return f'Задача №{self.num_doc} | {self.title} от {self.created_at}'