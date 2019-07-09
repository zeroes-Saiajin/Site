from model import *
sql_debug(True)


@db_session
def create_user():
    User(mail='maxdem4uk@yandex.ru', login='pascal', pwd='111', admin=True)


@db_session
def create_title():
    TvSeries(title='Звёздные войны', start='2019-01-01', description='фантастическая эпопея, включающая в себя 10 кинофильмов ('
                                                                                '8 эпизодов и 2 фильма "истории"), а также анимационные сериалы, '
                                                                                'мультфильмы, телефильмы, книги, комиксы, видеоигры, игрушки и прочие '
                                                                                'произведения, созданные в рамках единой фантастической вселенной «Звёздных '
                                                                                'войн», задуманной и реализованной американским режиссёром Джорджем Лукасом '
                                                                                'в конце 1970-х годов и позднее расширенной. ',
             image='https://www.gannett-cdn.com/-mm-/e3bce1a7b96dd36372f1f9a7b4e120623e931a52/c=0-68-1399-1120/local'
                   '/-/media/2015/12/08/USATODAY/USATODAY/635851909778644878-XXX-d-Star-Wars-CDs-ZX24463.jpg?width=520&height=390&fit=crop')


@db_session
def create_episode():
    titleseries = TvSeries.get(title='Звёздные войны')
    prod = Producer.get(first_name='Люк',last_name='Бессон')
    Episode(episode='1', season='1', title=titleseries, name='Новая надежда', date='2019-01-01', producer=prod)
    Episode(episode='2', season='1', title=titleseries, name='Империя наносит ответный удар', date='2019-02-02', producer=prod)


@db_session
def create_actor():
    s = TvSeries.get(title='Звёздные войны')
    ep = select(ep for ep in Episode if ep.season == 1 and ep.title == s and ep.episode == 1)[:]
    Actor(first_name='Лиам', last_name='Нисон', episodes=ep)
    ep = select(ep for ep in Episode if ep.season == 1 and ep.title == s and ep.episode == 2)[:]
    Actor(first_name='Николас', last_name='Кейдж', episodes=ep)


@db_session
def create_producer():
    Producer(first_name='Люк', last_name='Бессон')


@db_session
def create_score_series():
    use = User.get(id='1')
    ser = TvSeries.get(title='Звёздные войны')
    ScoreTitle(score_title=5, user=use, series=ser)


def main():
    from configuration import config
    db.bind(**config['PONY'])
    db.generate_mapping(create_tables=True)
    create_user()
    create_producer()
    create_title()
    create_episode()
    create_actor()
    create_score_series()


if __name__ == '__main__':
    main()
