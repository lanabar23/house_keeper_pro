from enum import auto
from django.db import models
from django.utils import timezone

from django.forms.fields import DateTimeField
from common_core.models  import Actions, Books, Categories, SubCategories, ActSubCategories

class UsersActions(models.Model):
    actcat = models.ForeignKey(
        'common_core.Categories',
        related_name='actcat',
        null=True,
        on_delete=models.SET_NULL, # , on_delete=models.CASCADE
        blank=True
    )
    actdone = models.ForeignKey(
        'common_core.ActSubCategories',
        related_name='actdone',
        null=True,
        on_delete=models.SET_NULL, # , on_delete=models.CASCADE
        blank=True
    )
    actstart = models.DateTimeField(default=timezone.now)
    actplandur = models.CharField(max_length=5)
    actfactdur = models.CharField(max_length=5, null=True)
    actstatus = models.CharField(choices=[
        ('online', 'онлайн'),
        ('offline','офлайн')
        ], default='online')
    actarea = models.CharField(choices=[
        ('inside', 'в помещении'),
        ('seatlace','на кресле'),
        ('bedlace','на диване'),
        ('outside','на улице')
        ], default='inside')
    actcoment = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.actdone


class ActionsFacts(models.Model):
    actdone = models.ForeignKey(
        'common_core.Actions',
        related_name='actdone',
        null=True,
        on_delete=models.SET_NULL, # , on_delete=models.CASCADE
        blank=True
    )
    actstart = models.DateTimeField(default=timezone.now)
    actfinish = models.DateTimeField(default=timezone.now)
    actstatus = models.CharField(choices=[
        ('online', 'онлайн'),
        ('offline','офлайн')
        ], default='online')
    actarea = models.CharField(choices=[
        ('inside', 'в помещении'),
        ('inplace','в кровати/на кресле'),
        ('outside','на улице')
        ], default='inside')
    actcoment = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.actdone
    

class BooksFacts(models.Model):
    # Модель для фиксирования работы с книгой в семейной библиотеке"""
    book_name = models.ForeignKey(
        'common_core.Books',
        related_name='bookdone',
        null=True,
        on_delete=models.SET_NULL,
        blank=True
    )
    timestart = models.DateTimeField(default=timezone.now)
    timefin = models.DateTimeField(default=timezone.now)
    pagestart = models.PositiveIntegerField()  # Стартовая страница
    pagefin = models.PositiveIntegerField()  # Финишная страница
    bookstatus = models.CharField(choices=[
        ('in_progress', 'в работе'),
        ('on_delay','отложена'),
        ('read','прочитана')
        ], default='inside')
    basic_thoughts = models.TextField(blank=True, null=True)  # Основные мысли
    coment = models.CharField(max_length=30, blank=True, null=True)  # Комментарий

    def __str__(self):
        # Возвращает строку, представляющую объект"""
        return f'{self.book_name}' 
    class Meta:
        ordering = ['book_name']  # сортировка по имени книги
