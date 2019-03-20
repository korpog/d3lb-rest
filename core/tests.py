from django.test import TestCase
from .models import Leaderboard


class LeaderboardCase(TestCase):

    @classmethod
    def setUp(cls):
        cls.lb1 = Leaderboard.objects.create(
            name="US Seasonal Softcore BR S1", region=Leaderboard.US, class_name=Leaderboard.BR, game_mode=Leaderboard.SS, season=1)

    def test_lb_name(self):
        lb = self.lb1
        self.assertEqual(lb.name, "US Seasonal Softcore BR S1")

    def test_lb_region(self):
        lb = self.lb1
        self.assertEqual(lb.region, "United States")

    def test_lb_classname(self):
        lb = self.lb1
        self.assertEqual(lb.class_name, "Barbarian")

    def test_lb_gamemode(self):
        lb = self.lb1
        self.assertEqual(lb.game_mode, "Seasonal Softcore")
