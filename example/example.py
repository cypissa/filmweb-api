""" Example of using the API class """

from filmweb_api import FilmwebApi

if __name__ == '__main__':
    filmweb_api = FilmwebApi('USERNAME', 'PASSWORD')
    filmweb_api.login()
    films = filmweb_api.get_user_films_want_to_see()
    print(films)

    films = filmweb_api.get_film_info_full(824633)
    print(films)
