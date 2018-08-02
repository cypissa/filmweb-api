""" Example of using the API class """

from filmweb_api import FilmwebApi

if __name__ == '__main__':
    filmweb_api = FilmwebApi('USER_USERNAME', 'USER_PASSWORD')
    filmweb_api.login()
    films = filmweb_api.get_user_film_votes()
    print(films)

    film_info = filmweb_api.get_film_info_full(films[3][0])
    print(film_info)
