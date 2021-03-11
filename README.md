[![Build Status](https://travis-ci.org/cypiszzz/filmweb-api.svg?branch=master)](https://travis-ci.org/cypiszzz/filmweb-api)

# Filmweb API

A package for utilizing filmweb's API.

Currently implemented methods:
* `login(username, password)`
* `get_user_film_votes(user_id)`
* `get_user_films_want_to_see(user_id)`
* `get_film_info_full(film_id)`

# Usage

## Login and logout

```
from filmweb_api import FilmwebApi

filmweb_api = FilmwebApi('USERNAME', 'PASSWORD')
filmweb_api.login()

print(filmweb_api.is_logged_in()) # True

filmweb_api.logout()

print(filmweb_api.is_logged_in()) # False
```

## Get films for a user

Get films for current logged in user:

```
from filmweb_api import FilmwebApi

filmweb_api = FilmwebApi('USERNAME', 'PASSWORD')
filmweb_api.login()

films = filmweb_api.get_user_film_votes()
```

Get films for a user with specified id (logged user has to have permissions to see another user's films):
```
from filmweb_api import FilmwebApi

user_id = 123456
filmweb_api = FilmwebApi('USERNAME', 'PASSWORD')
filmweb_api.login()

films = filmweb_api.get_user_film_votes(user_id)
```

## Get films a user wants to see

Get films a user wants to see for current logged in user:

```
from filmweb_api import FilmwebApi

filmweb_api = FilmwebApi('USERNAME', 'PASSWORD')
filmweb_api.login()

films = filmweb_api.get_user_films_want_to_see()
```

Get films a user wants to see for a user with specified id (logged user has to have permissions to see another user's films):
```
from filmweb_api import FilmwebApi

user_id = 123456
filmweb_api = FilmwebApi('USERNAME', 'PASSWORD')
filmweb_api.login()

films = filmweb_api.get_user_films_want_to_see(user_id)
```

## Get film full info

```
from filmweb_api import FilmwebApi

filmweb_api = FilmwebApi('USERNAME', 'PASSWORD')
filmweb_api.login()

films = filmweb_api.get_film_info_full(user_id)
```


# Development

Get poetry:
```
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py
python ./get-poetry.sh --preview -y
```

Install deps:
```
poetry install --dev
```
