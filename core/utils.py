import json
import datetime
from .models import Record, Leaderboard
import requests
from django.utils.text import slugify
from django.utils.timezone import make_aware
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


regions = ['us', 'eu', 'kr']
classes = ['barbarian', 'necromancer', 'crusader', 'dh',
           'monk', 'wd', 'wizard']
game_modes = ['', 'hardcore-']
current_season = 16


def get_access_token():
    """ Get access token required to use Blizzard's API. """
    with open('credentials.json', 'r') as file:
        credentials = json.load(file)

    client_id = credentials['CLIENT_ID']
    client_secret = credentials["CLIENT_SECRET"]

    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url='https://us.battle.net/oauth/token', client_id=client_id,
                              client_secret=client_secret)
    access_token = token['access_token']
    return access_token


def get_data(access_token, region, class_name, season, game_mode=''):
    """
    Get data from Blizzard's API. Returns a Python object representing JSON data.

    Allowed argument values:
    region: us, eu, kr
    class_name: barbarian, dh, monk, wizard, wd, necromancer
    season: 1 to 16 (as of February 2019)
    gamemode: 'hardcore-' or '' (default value)

    """
    r = requests.get(
        f'https://{region}.api.blizzard.com/data/d3/season/{season}/leaderboard/rift-{game_mode}{class_name}?access_token={access_token}')
    data = json.loads(r.text)
    return data


def process_data(leaderboard, data):
    """ Get leaderboard data and save it into a database """
    Record.objects.filter(leaderboard_id=leaderboard.id).delete()
    records = []
    for row in data['row']:
        battletag = row['player'][0]['data'][0].get('string', 'unknown')
        class_name = row['player'][0]['data'][2]['string']
        rank = row['data'][0]['number']
        rift_level = row['data'][1]['number']
        rift_time = datetime.timedelta(
            milliseconds=row['data'][2]['timestamp'])
        date = row['data'][3]['timestamp'] / 1000
        date = make_aware(datetime.datetime.utcfromtimestamp(date))
        record = Record(rank=rank, battletag=battletag, class_name=class_name, rift_level=rift_level,
                        rift_time=rift_time, completed_on=date, leaderboard=leaderboard)
        records.append(record)
    Record.objects.bulk_create(records)


def create_leaderboards():
    """ Create leaderboards for every region, class and game mode """
    token = get_access_token()
    for region in regions:
        for class_name in classes:
            for game_mode in game_modes:
                for i in range(16, 17):
                    if (class_name == 'necromancer' and i < 11):
                        pass
                    else:
                        slug = slugify(
                            f'{region} {class_name} {game_mode} s{i}')
                        print(slug)
                        Leaderboard(slug=slug, region=region,
                                    class_name=class_name, game_mode=game_mode, season=i).save()
                        data = get_data(token, region, class_name,
                                        i, game_mode=game_mode)
                        lb = Leaderboard.objects.get(slug=slug)
                        process_data(lb, data)


def create_solo_lb():
    """ Get a Top 1000 records from all classes for a given region, game mode and season """
    for region in regions:
        for game_mode in game_modes:
            for i in range(16, 17):
                solo_lb = Leaderboard(slug=f'{region}-solo-{game_mode}s{i}', region=region,
                                      class_name='solo', game_mode=game_mode, season=i)
                solo_lb.save()
                for class_name in classes:
                    if (class_name == 'necromancer' and i < 11):
                        pass
                    else:
                        print(f'{region}-{class_name}-{game_mode}s{i}')
                        lb = Leaderboard.objects.get(
                            slug=f'{region}-{class_name}-{game_mode}s{i}')
                        qs = Record.objects.filter(
                            leaderboard_id=lb.id).order_by('rank')[:1001]
                        for q in qs:
                            r = Record(id=None, rank=q.rank, battletag=q.battletag, class_name=q.class_name,
                                       rift_level=q.rift_level, rift_time=q.rift_time,
                                       completed_on=q.completed_on, leaderboard=solo_lb)
                            r.save()
                qs = Record.objects.filter(leaderboard_id=solo_lb.id).order_by(
                    '-rift_level', 'rift_time')
                for i, q in enumerate(qs):
                    q.rank = i + 1
                    q.save()


def update_leaderboards(season):
    token = get_access_token()
    for region in regions:
        for game_mode in game_modes:
            for class_name in classes:
                if (class_name == 'necromancer' and season < 11):
                    pass
                else:
                    data = get_data(token, region, class_name, season)
                    lb = Leaderboard.objects.get(
                        slug=f'{region}-{class_name}-{game_mode}s{season}')
                    process_data(lb, data)

    for region in regions:
        for game_mode in game_modes:
            solo_lb = Leaderboard.objects.get(
                slug=f'{region}-solo-{game_mode}s{season}')
            Record.objects.filter(leaderboard_id=solo_lb.id).delete()
            for class_name in classes:
                if (class_name == 'necromancer' and season < 11):
                    pass
                else:
                    lb = Leaderboard.objects.get(
                        slug=f'{region}-{class_name}-{game_mode}s{season}')
                    qs = Record.objects.filter(
                        leaderboard_id=lb.id).order_by('rank')[:1001]
                    for q in qs:
                        r = Record(id=None, rank=q.rank, battletag=q.battletag, class_name=q.class_name,
                                   rift_level=q.rift_level, rift_time=q.rift_time,
                                   completed_on=q.completed_on, leaderboard=solo_lb)
                        r.save()
            qs = Record.objects.filter(leaderboard_id=solo_lb.id).order_by(
                '-rift_level', 'rift_time')
            for i, q in enumerate(qs):
                q.rank = i + 1
                q.save()
    cleanup = Record.objects.filter(rank__gt=50)
    cleanup.delete()
