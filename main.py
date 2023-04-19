from flask import Flask, render_template, redirect, request
import os
from werkzeug.utils import secure_filename

from data import db_session

from data.films import Films
from data.genres_films import GenreFilm
from data.performers import Performers
from data.music import Music
from data.users import User

from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from forms.add_movie_form import AddMovie

from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init('db/info.sqlite')
    app.run()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/movie')
def movie():
    return render_template('movie.html')


@app.route('/genre')
def genre():
    db_sess = db_session.create_session()

    cur_genre = request.args.get('name')
    index_genre = db_sess.query(GenreFilm).filter(
        GenreFilm.title == cur_genre).first().id

    films = db_sess.query(Films).filter(Films.genre == index_genre)

    list_films = []

    for film in films:
        list_films.append(dict(title=film.title, image=film.image))

    return render_template('genre.html', list_films=list_films)


@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():

    form = AddMovie()

    if form.validate_on_submit():

        # Сохранение изображения в директорию с остальными обложками фильмов
        file = form.image.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                  f'static/img/films/{form.genre.data}', secure_filename(file.filename)))
        # ------------------------------------------------------------------

        db_sess = db_session.create_session()

        film = Films(
            title=form.title.data,
            info=form.about.data,
            genre=db_sess.query(GenreFilm).filter(
                GenreFilm.title == form.genre.data.lower()).first().id,
            duration=form.duration.data,
            director=form.director.data,
            production=form.production.data,
            premiere=form.premiere.data,
            budget=form.budget.data,
            image=f'/img/films/{form.genre.data}/{file.filename}',
            user_id=db_sess.query(User).filter(
                User.name == current_user.name).first().id
        )

        db_sess.add(film)
        db_sess.commit()

        return redirect('/')

    return render_template('add_movie.html', form=form)


@app.route('/movie_info')
def movie_info():

    cur_title = request.args.get('film_name')

    db_sess = db_session.create_session()
    cur_movie = db_sess.query(Films).filter(Films.title == cur_title).first()
    cur_genre = db_sess.query(GenreFilm).filter(
        GenreFilm.id == cur_movie.genre).first().title

    author_id = db_sess.query(Films).filter(
        Films.title == cur_title).first().user_id

    if author_id:
        name_author = db_sess.query(User).filter(
            User.id == author_id).first().name
    else:
        name_author = None

    movie_params = {
        'title': cur_title,
        'image': cur_movie.image,
        'genre': cur_genre,
        'director': cur_movie.director,
        'production': cur_movie.production,
        'premiere': cur_movie.premiere,
        'year': cur_movie.premiere.split(', ')[1],
        'budget': cur_movie.budget,
        'duration': f'{int(cur_movie.duration) // 60}h {int(cur_movie.duration) % 60}m',
        'about': cur_movie.info,
        'name_author': name_author,
    }

    return render_template('movie_info.html', movie_params=movie_params)


@app.route('/performers')
def performers():
    db_sess = db_session.create_session()

    perf_cover = []

    for performer in db_sess.query(Performers).all():
        perf_cover.append(
            dict(name=performer.name, image=performer.image))

    return render_template('performers.html', perf_cover=perf_cover)


@app.route('/performer_info')
def performer_info():
    db_sess = db_session.create_session()

    cur_name = request.args.get('name')

    cur_performer = db_sess.query(Performers).filter(
        Performers.name == cur_name).first()

    perf_params = {
        'name': cur_performer.name,
        'image': cur_performer.image,
        'genres': cur_performer.genre,
        'activity': cur_performer.activity,
        'about': cur_performer.about
    }

    return render_template('performer_info.html', perf_params=perf_params)


@app.route('/music')
def music():
    db_sess = db_session.create_session()
    cur_period = request.args.get('period')

    music_params = []

    if cur_period:
        music_list = db_sess.query(Music).filter(Music.period == cur_period)
    else:
        music_list = db_sess.query(Music).all()

    for music in music_list:
        music_params.append(dict(track_name=music.track_name, path=music.path))

    return render_template('music.html', music_params=music_params)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form, message='Password mismatch')

        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', form=form, message='Such user already exists')

        user = User(
            name=form.name.data,
            email=form.email.data
        )

        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        return redirect('/login')

    return render_template('register.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()

    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')

        return render_template('login.html', form=form, message='Incorrect login or password')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect('/')


if __name__ == '__main__':
    main()
