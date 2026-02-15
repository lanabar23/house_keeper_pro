from django.db import models
from django.utils import timezone
from django.forms import BooleanField, CharField
from django.urls import base


class KeeperApps(models.Model):
    appname = models.CharField(max_length=50) 
    applabel =  models.CharField(max_length=50)

    def __str__(self):
        return self.applabel

class FamilyUsers(models.Model):
    username = models.CharField(max_length=40) 
    usernick =  models.CharField(max_length=2)

    def __str__(self):
        return self.usernick

class ActsCategories(models.Model):
    actscategory = models.CharField(max_length=30)
    def __str__(self):
        return self.actscategory

class ActSubCategories(models.Model):
    actsubcategory = models.CharField(max_length=150)
    actscategory = models.ForeignKey(
        'ActsCategories',
        related_name='actsub',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    actstatus = models.CharField(choices=[
        ('online', 'онлайн'),
        ('offline','офлайн')
        ], default='online')
    addactdate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.actsubcategory
    
class Actions(models.Model):
    action = models.CharField(max_length=150)
    keeperapps = models.ForeignKey(
        'KeeperApps',
        related_name='actapps',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    actionprd = models.ForeignKey(
        'Periods',
        related_name='actprds',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.action
    



class QueryAnswers(models.Model):
    shortquery = models.CharField(max_length=255)
    fullquery = models.TextField()
    appsname = models.ForeignKey(
        KeeperApps,
        related_name='projectapp',
        on_delete=models.CASCADE, # SET_NULL,
        null=True,
        blank=True
    )
    is_urgent = models.BooleanField(default=False) 
    source = models.CharField(max_length=255)
    asktime = models.DateTimeField(auto_now_add=True)
    resolvetime = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[
        ('in_progress', 'В работе'),
        ('resolved', 'Решен'),
        ('deferred', 'Отложен'),
    ], default='in_progress')
    resansways = models.TextField()
    resansfact = models.TextField()  # resolve - answer
    coment = models.CharField(max_length=255)

class Actives(models.Model):
    account_num = models.IntegerField()
    owner_name = models.ForeignKey(
        'FamilyUsers',
        related_name='owners',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    account_finorg = models.ForeignKey(
        'Organizations',
        related_name='accounts',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    account_country = models.CharField(max_length=150, default='РФ')
    account_type = models.CharField(choices=[
        ('payment', 'расчетный'),
        ('card', 'дебетовая карта'),
        ('savings ','накопительный'),
        ('deposit', 'вклад/депозит'),
        ('broker','брокерский'),
        ('invest','инвестиционный'),
        ('depo', 'депозитарный'),
        ('credit', 'кредитный'),
        ('ndd', 'not dealing desk'),
        ('direct', 'direct'),
        ], default='card')
    account_owner = models.CharField(choices=[
        ('individual', 'Физическое лицо'),              # Персональный счёт
        ('legal_entity', 'Юридическое лицо')            # Организация/субъект бизнеса
        ],
        default='individual'                                # Значение по умолчанию
    )
    account_currency = models.CharField(choices=[
        ('RUR', 'руб'),
        ('USD', 'долл сша'),
        ('EUR', 'евро'),
        ('USDT', 'крипто долл'),
        ], default='RUR'                                # Значение по умолчанию
    ) 
    account_curtype = models.CharField(choices=[
        ('fiat', 'фиат'),
        ('cripto', 'крипто'),
        ('stocks', 'акции'),
        ('bonds', 'облигации'),
        ('objects', 'объекты'),
        ], default='fiat'
    )
    is_cardlinked = models.BooleanField(default=False)
    # Текущая сумма на счете
    account_sum = models.DecimalField(max_digits=15, decimal_places=2)    
    # Дата открытия счёта
    account_opendate = models.DateField(default=timezone.now)
    # Известен ФНС
    is_fnsknown = models.BooleanField(default=False)
    account_coment = models.CharField(max_length=150, null=True)
    
    def __str__(self):
        return f"{self.account_finorg}: {self.account_type} №{self.account_num}"



class Organizations(models.Model):
    org_name = models.CharField(max_length=250)
    org_type = models.CharField(choices=[
        ('bank','банк'),
        ('broker','брокер'),
        ('dealer','дилер'),
        ('fxdealer','форекс-дилер'),
        ('fond','фонд'),
        ('ratingagency','РА'),
        ('insurance','страховая компания'),
        ('creditbureau','кредитное бюро'),
        ('finteh','финтех'),
        ('stockmarket','биржа'),
        ('cryptomarket','криптобиржа'),
        ('forex','форекс'),
        ('realestate','недвижимость'),
        ('market','торговая сеть'),
        ('medical','медучреждение'),
        ], default='bank'
    )
    org_legal = models.CharField(max_length=150, default='РФ')
    org_url = models.URLField(null=True)

    def __str__(self):
        return self.org_name

class Notes(models.Model):
    note_date = models.DateField(auto_now_add=True)
    note_type = models.CharField(choices = [
        ('note', 'заметка'),
        ('thought', 'размышление'),
        ('task', 'задача'),
        ], default='task')
    note_category = models.ForeignKey(
        'KeeperApps',
        related_name='notesapps',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    note_text = models.TextField()

class SubCategories(models.Model):
    prodname = models.CharField()
    prodcategory = models.ForeignKey(
        'Categories',
        related_name='prods',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    prodbasket = models.CharField(choices=[
        ('base','базовый'),
        ('standart','стандартный'),
        ('upstandart','расширенный'),
        ('premium','премиальный'),
        ],default='base')
    prodcoment = models.CharField(max_length=250, null=True)
    is_nesessary = models.BooleanField(default=False)
    def __str__(self):
        return self.prodname   
    

class Categories(models.Model):
    catname = models.CharField(max_length=150)
    catbuhtype = models.CharField(choices=[
        ('action','действие'),
        ('event','событие'),
        ],default='action')
    catusertype = models.CharField(choices=[
        ('profit','поступления'),
        ('payments','выплаты'),
        ('products','товары'),
        ('services','услуги'),
        ], default='')
    catstatus = models.CharField(choices=[
        ('constant', 'постоянный'),
        ('temporary', 'временный'),
        ('discret', 'дискретный'),
        ], default='')
    catperiod = models.ForeignKey(
        'Periods',
        related_name='prds',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.catname   
    
class Periods(models.Model):
    prdname = models.CharField(max_length=50)
    def __str__(self):
        return self.prdname   
 

class Books(models.Model):
    # Поля базы данных
    book_name = models.CharField(max_length=200)  # Имя книги
    tag_name = models.CharField(max_length=50, blank=True, null=True)  # Теги
    kind_of_book = models.CharField(choices=[
        ('print', 'печатная'),
        ('digit', 'электронная'),
        ], default='print')  # Вид книги
    author = models.CharField(max_length=100)  # Автор
    pages = models.PositiveIntegerField(null=True)  # Количество страниц
    subject = models.CharField(max_length=100, null=True)  # Область знаний
    publ_seria = models.CharField(max_length=100, blank=True, null=True)  # Серия публикации
    is_q_and_exc = models.BooleanField(default=False)  # Признак наличия вопросов и упражнений
    is_answers = models.BooleanField(default=False)  # Признак наличия ответов
    is_verified = models.BooleanField(db_default=False) 
    buydate = models.DateField(default=timezone.now)  # Дата начала чтения
    bookcost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    timestart = models.DateField(blank=True, null=True)  # Дата начала чтения
    timefin_plan = models.DateField(blank=True, null=True)  # Планируемая дата завершения
    timefin_fact = models.DateField(blank=True, null=True)  # Фактическая дата завершения
    rating = models.IntegerField(null=True)  # Рейтинг книги
    basic_thoughts = models.TextField(blank=True, null=True)  # Основные мысли
    publ_year = models.IntegerField(null=True)  # Год издания
    publ_house = models.CharField(max_length=100, null=True)  # Издательство
    publ_city = models.CharField(max_length=100, blank=True, null=True)  # Город издательства
    coment = models.CharField(max_length=30, blank=True, null=True)  # Комментарий

    def __str__(self):
        # Возвращает строку, представляющую объект"""
        return f'{self.book_name} {self.author}'

    class Meta:
        ordering = ['book_name']  # сортировка по имени книги


class Plans(models.Model):
    nameplan = models.CharField(max_length=150, default='План')
    plan_type = models.CharField(choices = [
        ('shortprd', 'краткосрочный'),
        ('mediumprd', 'среднесрочный'),
        ('longprd', 'долгосрочный'),
        ])
    start_date = models.DateField(default=timezone.now)
    finish_date = models.DateField(default=timezone.now)
    create_date = models.DateTimeField(auto_now_add=True)



 