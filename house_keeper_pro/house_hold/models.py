from django.db import models

class FamilyLibrary(models.Model):
    # Модель для представления книг в семейной библиотеке"""

    # Поля базы данных
    book_name = models.CharField(max_length=200)  # Имя книги
    tag_name = models.CharField(max_length=50, blank=True, null=True)  # Теги
    kind_of_book = models.CharField(max_length=50, blank=True, null=True)  # Вид книги
    author = models.CharField(max_length=100)  # Автор
    pages = models.PositiveIntegerField()  # Количество страниц
    subject = models.CharField(max_length=100)  # Область знаний
    publ_seria = models.CharField(max_length=100, blank=True, null=True)  # Серия публикации
    is_q_and_exc = models.BooleanField(default=False)  # Признак наличия вопросов и упражнений
    is_answers = models.BooleanField(default=False)  # Признак наличия ответов
    timestart = models.DateField(blank=True, null=True)  # Дата начала чтения
    timefin_plan = models.DateField(blank=True, null=True)  # Планируемая дата завершения
    timefin_fact = models.DateField(blank=True, null=True)  # Фактическая дата завершения
    rating = models.IntegerField()  # Рейтинг книги
    basic_thoughts = models.TextField(blank=True, null=True)  # Основные мысли
    publ_year = models.IntegerField()  # Год издания
    publ_house = models.CharField(max_length=100)  # Издательство
    publ_city = models.CharField(max_length=100, blank=True, null=True)  # Город издательства
    coment = models.CharField(max_length=30, blank=True, null=True)  # Комментарий

    def __str__(self):
        # Возвращает строку, представляющую объект"""
        return f'{self.book_name} {self.author}'

    class Meta:
        ordering = ['book_name']  # сортировка по имени книги
