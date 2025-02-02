from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

        # Упорядочивание по дате публикации по убыванию
        ordering = ['-published_at']

    def __str__(self):
        return self.title
    

class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    articles = models.ManyToManyField(Article, through='Scope', related_name='tags', verbose_name='Статьи')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Scope(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes', verbose_name='Статья')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='scopes', verbose_name='Тег')

    is_main = models.BooleanField(default=False, verbose_name='Основной')

    class Meta:
        verbose_name = 'Тематика статьи'
        verbose_name_plural = 'Тематики статьи'

        # Основной тег идет первым, остальные — в алфавитном порядке
        ordering = ['-is_main', 'tag__name']    

    def __str__(self):
        return f'{self.article.title} - {self.tag.name}'
    
