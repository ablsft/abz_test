from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Position(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название должности')
    hierarchy_level = models.IntegerField(default=1, 
                        validators=[MinValueValidator(1), MaxValueValidator(5)],
                        verbose_name='Уровень иерархии')
    

class Employee(models.Model):
    full_name = models.CharField(max_length=60, verbose_name='ФИО')
    position = models.ForeignKey(Position, on_delete=models.CASCADE,
                        verbose_name='Должность', related_name='employees')
    employment_date = models.DateField(verbose_name='Дата приёма на работу')
    salary = models.IntegerField(verbose_name='Размер заработной платы')
    manager = models.ForeignKey('self', on_delete=models.CASCADE,
                        verbose_name='Начальник', related_name='subordinates')