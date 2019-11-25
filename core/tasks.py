from __future__ import absolute_import, unicode_literals
from celery import Celery
from d3leaderboards.celery import app
from .utils import update_leaderboards
from .models import Leaderboard

@app.task
def update_lb():
    update_leaderboards(19)
    print("Leaderboards updated!")


app.conf.beat_schedule = {
    "update-leaderboards-task": {
        "task": "core.tasks.update_lb",
        "schedule": 86400.0
    }
}
