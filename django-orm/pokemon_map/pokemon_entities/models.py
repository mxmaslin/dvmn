from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    title_en = models.CharField(
        max_length=200,
        verbose_name='Название на английском',
        default='',
        blank=True
    )
    title_jp = models.CharField(
        max_length=200,
        verbose_name='Название на японском',
        default='',
        blank=True
    )
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    description = models.TextField(
        default='', blank=True, verbose_name='Описание'
    )
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolutions',
        verbose_name='Из кого эволюционировал'
    )

    @property
    def pokemon_id(self):
        return self.id

    @property
    def img_url(self):
        return self.image.url

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    latitude = models.FloatField(verbose_name='Широта', null=True, blank=True)
    longitude = models.FloatField(verbose_name='Долгота', null=True, blank=True)
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='Покемон',
        related_name='pokemon_entities'
    )
    appeared_at = models.DateTimeField(
        verbose_name='Когда появился', null=True, blank=True
    )
    disappeared_at = models.DateTimeField(
        null=True, blank=True, verbose_name='Когда исчезнет'
    )
    level = models.IntegerField(
        default=0, verbose_name='Уровень', null=True, blank=True
    )
    health = models.IntegerField(
        default=1, verbose_name='Здоровье', null=True, blank=True
    )
    strength = models.IntegerField(
        default=1, verbose_name='Сила', null=True, blank=True
    )
    defence = models.IntegerField(
        default=1, verbose_name='Защита', null=True, blank=True
    )
    stamina = models.IntegerField(
        default=1, verbose_name='Выносливость', null=True, blank=True
    )

    def __str__(self):
        return f'{self.pokemon}, {self.level}'


