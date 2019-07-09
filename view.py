from app import app
from flask_login import login_user, current_user, logout_user, login_required
from model import db
from form_request import *
from pony.orm import select, commit, flush, desc, sql_debug
from flask import render_template, request, flash, redirect, url_for
from datetime import datetime

@app.route('/')
@login_required
def index():
    return redirect(url_for('series'))

@app.route('/404')
def error_404():
    return "Запрашиваемая страница не существует"


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        login = form.login.data
        mail = form.mail.data
        pwd = form.pwd.data
        t = db.User(
            login=login,
            mail=mail,
            pwd=pwd
        )
        titles = db.TvSeries.select()[:]
        for titl in titles:
            db.ScoreTitle(user=t, series=titl)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        login = form.login.data
        pawd = form.pwd.data
        user = db.User.get(login=login)
        if user.pwd != pawd:
            form.pwd.errors = ['Неверный пароль']
            return render_template('login.html', form=form)
        login_user(user, remember=True, force=True)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    user = current_user
    user.load()
    return render_template('profile.html', user=user)


@app.route('/actor_new', methods=["POST", "GET"])
@login_required
def actor_new():
    user = current_user
    form = NameForm(request.form)
    if request.method == "POST" and form.validate():
        db.Actor(first_name=form.first_name.data, last_name=form.last_name.data)
        return redirect(url_for('actor_new'))
    return render_template('actor_new.html', form=form, user=user)


@app.route('/producer_new', methods=["POST", "GET"])
@login_required
def producer_new():
    user = current_user
    form = NameForm(request.form)
    if request.method == "POST" and form.validate():
        db.Producer(first_name=form.first_name.data, last_name=form.last_name.data)
        return redirect(url_for('producer_new'))
    return render_template('producer_new.html', form=form, user=user)


@app.route('/series')
@login_required
def series():
    user = current_user
    titles = db.TvSeries.select()[:]
    return render_template('series.html', seriess=titles, user=user)


@app.route('/tseries/<int:id>')
@login_required
def tseries(id):
    user = current_user
    tseries = db.TvSeries.get(id=id)
    ep = select(s for s in db.Episode if s.title == tseries).order_by(db.Episode.season)
    st = db.ScoreTitle.get(series=tseries, user=user.id)
    return render_template('tseries.html', tseries=tseries, episod=ep, user=user, st=st)


@app.route('/score', methods=['POST'])
def score_title():
    id_ = request.form['id']
    value_ = request.form['value']
    st = db.ScoreTitle.get(id=id_)
    st.score_title = value_
    commit()
    return 'ok'


@app.route('/episode/<int:id>')
@login_required
def episode(id):
    user = current_user
    s = select(s for s in db.Episode if s.id == id).prefetch(db.TvSeries).first()
    actors = s.actors
    return render_template('episode.html', ep=s, user=user, prod=s.producer, actors=actors)


@app.route('/series/new', methods=["POST", "GET"])
@login_required
def title_new():
    user = current_user
    form = TitleForm(request.form)
    if request.method == "POST" and form.validate():
        start = request.form['date']
        if not start:
            return render_template('title_new.html', form=form, user=user)

        t = db.TvSeries(title=form.title.data, description=form.description.data, image=form.image.data, start=start)
        us = db.User.select()[:]
        for u in us:
            db.ScoreTitle(user=u, series=t)
        return redirect(url_for('series'))
    return render_template('title_new.html', form=form, user=user)


@app.route('/episode/new', methods=["POST", "GET"])
@login_required
def episode_new():
    user = current_user
    form = EpisodeForm(request.form)
    form.title.choices = select((t.title, t.title) for t in db.TvSeries)[:]
    form.prod.choices = select((p.first_name, p.first_name) for p in db.Producer)[:]
    actors = db.Actor.select()[:]
    if request.method == "POST" and form.validate():
        episode = form.episode.data
        season = form.season.data
        title = form.title.data
        actorss = request.form.getlist('actors')
        prod = db.Producer.get(first_name=form.prod.data)
        idd = db.TvSeries.get(title=title)
        date = request.form['date']
        prov = select(ep for ep in db.Episode if ep.episode == episode and ep.season == season and ep.title == idd)
        if prov:
            return render_template('episode_new.html', form=form, user=user, actors=actors,
                                   error='Такой эпизод уже существует')
        elif not date:
            return render_template('episode_new.html', form=form, user=user, actors=actors,
                                   error='Нужна дата')

        epp = db.Episode(name=form.name.data, episode=episode, season=season, title=idd, date=date, producer=prod)
        for actor in select(g for g in db.Actor if g.first_name in actorss):
            actor.episodes.add(epp)

        return redirect(url_for('series'))
    return render_template('episode_new.html', form=form, user=user, actors=actors)
