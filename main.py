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

    print(list_films)

    return render_template('genre.html', list_films=list_films)


if __name__ == '__main__':
    main()
