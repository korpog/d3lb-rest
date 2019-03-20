from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Leaderboard(models.Model):
    US = 'United States'
    EU = 'Europe'
    KR = 'Korea'
    REGIONS = (
        (US, 'United States'), (EU, 'Europe'), (KR, 'Korea')
    )

    DH = 'Demon Hunter'
    BR = 'Barbarian'
    WD = 'Witch Doctor'
    MN = 'Monk'
    NC = 'Necromancer'
    WZ = 'Wizard'
    SOLO = 'Solo'
    CLASSES = (
        (DH, 'Demon Hunter'), (BR, 'Barbarian'), (WD, 'Witch Doctor'),
        (MN, 'Monk'), (NC, 'Necromancer'), (WZ, 'Wizard'), (SOLO, 'Solo')
    )

    SS = 'Season'
    SH = 'Season HC'
    NS = 'Nonseason'
    NH = 'Nonseason HC'
    GAME_MODES = (
        (SS, 'Seasonal Softcore'), (SH, 'Seasonal Hardcore'),
        (NS, 'Nonseasonal Softcore'), (NH, 'Nonseasonal Hardcore')
    )

    slug = models.SlugField(max_length=150, default='default-slug')
    region = models.CharField(max_length=50, choices=REGIONS, default=US)
    class_name = models.CharField(max_length=50, choices=CLASSES, default='BR')
    game_mode = models.CharField(
        max_length=15, choices=GAME_MODES, default='SS')
    season = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(16)], default=1)

    def __str__(self):
        return self.slug


class Record(models.Model):
    leaderboard = models.ForeignKey(
        Leaderboard, on_delete=models.CASCADE, related_name='records')
    class_name = models.CharField(max_length=50)
    battletag = models.CharField(max_length=50)
    rank = models.IntegerField()
    rift_level = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(150)])
    rift_time = models.DurationField()
    completed_on = models.DateTimeField(verbose_name='Rift completed on')

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return f'{self.battletag} GR{self.rift_level} {self.completed_on}'
