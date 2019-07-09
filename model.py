from datetime import date
from pony.orm import *
from flask_login import UserMixin

db = Database()


class TvSeries(db.Entity):
    title = Required(str, unique=True)
    description = Required(str)
    image = Required(str)
    seasons = Set('Episode')
    start = Required(date)
    score_titles = Set('ScoreTitle')


class User(db.Entity, UserMixin):
    id = PrimaryKey(int, auto=True)
    mail = Required(str, unique=True)
    login = Required(str, unique=True)
    pwd = Required(str)
    score_title = Set('ScoreTitle')
    admin = Required(bool, default=False)
    activated = Required(bool, default=True)

    def is_admin(self):
        return self.admin


class Episode(db.Entity):
    name = Required(str)
    episode = Required(str)
    season = Required(str)
    actors = Set('Actor')
    title = Required(TvSeries)
    producer = Required('Producer')
    date = Required(date)


class Actor(db.Entity):
    id = PrimaryKey(int, auto=True)
    first_name = Required(str)
    last_name = Optional(str)
    episodes = Set(Episode)


class Producer(db.Entity):
    id = PrimaryKey(int, auto=True)
    first_name = Required(str)
    last_name = Optional(str)
    episodes = Set(Episode)


class ScoreTitle(db.Entity):
    score_title = Optional(int)
    user = Required(User)
    series = Required(TvSeries)




