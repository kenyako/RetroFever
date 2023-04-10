from flask import Flask, render_template, redirect, request
from data import db_session
from data.films import Films
from data.genres_films import GenreFilm


app = Flask(__name__)


def main():
    db_session.global_init('db/categories.sqlite')
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


@app.route('/movie_info')
def movie_info():

    cur_title = request.args.get('film_name')

    db_sess = db_session.create_session()
    cur_movie = db_sess.query(Films).filter(Films.title == cur_title).first()

    cur_genre = db_sess.query(GenreFilm).filter(
        GenreFilm.id == cur_movie.genre).first().title

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
    }

    return render_template('movie_info.html', movie_params=movie_params)


if __name__ == '__main__':
    main()
