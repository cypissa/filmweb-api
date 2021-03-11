# -*- coding: utf-8 -*-
""" Class for using filmweb's API """

import re
import ast
import hashlib
import urllib
from requests import session
from .config import Config
from .exceptions import LoginFailedException, NoActiveUserSessionException, WrongArgumentException


class FilmwebApi:
    """
    filmweb_api = FilmwebApi('username', 'password') # standard session_service is provided
    # or
    filmweb_api = FilmwebApi('username', 'password', session_service=session_service)
    # or
    filmweb_api = FilmwebApi('username', 'password', config={
        'USER_AGENT': 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'
        'API_HOST' = 'https://ssl.filmweb.pl/api?'
        'API_VERSION' = '1.0'
        'APP_ID' = 'android'
        'APP_KEY' = 'qjcGhW2JnvGT9dfCt3uT_jozR3s'
    })

    filmweb_api.login()                      # login using config's credentials
    filmweb_api.login(username, password)    # login using username and password
    filmweb_api.logout()                     # close current session
    filmweb_api.get_user_film_votes()        # retrieve film votes for currently logged user
    filmweb_api.get_user_film_votes(user_id) # retrieve film votes for user_id
                                             # (login is still required)
    filmweb_api.get_film_info_full(film_id)  # get full info of film_id
    """

    _config = None
    _session = None
    _request_headers = None

    _app_user_id = None

    def __init__(self, username, password, session_service=None, settings=None):
        """ Initialize instance

        config - Config object containing necessary consts
        session_service - session service (eg. provided by requests.session() factory)
        """

        if settings is None:
            settings = {}

        if not isinstance(settings, dict):
            raise WrongArgumentException('Settings argument has to be a dictionary')

        settings['username'] = username
        settings['password'] = password

        self._config = Config(settings)

        self._request_headers = {
            'User-Agent': self._config.user_agent
        }

        if session_service is None:
            self._session = session()
        else:
            self._session = session_service

    def login(self, username=None, password=None):
        """ Login

        username - if present override username from the config
        password - if present override username from the config

        Returns:
            [username, avatar, name, user_id, gender]
        """

        self.logout()

        if username is None:
            username = self._config.username
        if password is None:
            password = self._config.password

        if username is None or password is None:
            raise WrongArgumentException('You must provide username and password')

        method = 'login ["' + username + '", "' + password + '", 1]\n'

        target_url, params = self._prepare(method)
        response = self._session.post(target_url, params, headers=self._request_headers)

        data = self._parse_content(response.content)

        if not response.cookies or not isinstance(data, list) or not data[3]:
            raise LoginFailedException('Login failed. Please check credentials.')

        self._app_user_id = int(data[3])

    def logout(self):
        """ Close session """

        self._app_user_id = None
        self._session.cookies.clear()

    def is_logged_in(self):
        """ Check whether there is a user logged in """

        if self._app_user_id is not None:
            return True
        return False

    def get_user_film_votes(self, user_id=None):
        """ Get all user's votes

        user_id - if present override currently logged user_id

        Returns:
            [
                [film_id, seen_date, rate, favorite, comment, film_type]
                # ...
            ]
        """

        if self.is_logged_in():
            votes_user_id = self._app_user_id
        else:
            raise NoActiveUserSessionException('There is no active session. Please use \'login\' method first.')

        if user_id is not None:
            votes_user_id = user_id

        return self._fire_method('getUserFilmVotes [' + str(votes_user_id) + ', 1]')

    def get_user_films_want_to_see(self, user_id=None):
        """ Get user's films they want to see

        user_id - if present override currently logged user_id

        Returns:
            [
                [film_id, timestamp, level, film_type]
                # ...
            ]
        """

        if self.is_logged_in():
            votes_user_id = self._app_user_id
        else:
            raise NoActiveUserSessionException('There is no active session. Please use \'login\' method first.')

        if user_id is not None:
            votes_user_id = user_id

        return self._fire_method('getUserFilmsWantToSee [' + str(votes_user_id) + ', 1]')

    def get_film_info_full(self, film_id):
        """ Get full info of a film

        film_id - id of the film

        Returns:
            [
                title, original_title, rate, votes_count, genres, year, duration, comments_count,
                forum_url, has_review, has_description, image_path, video, premiere_world,
                premiere_country, film_type, seasons_count, episodes_count, countries_string,
                synopsis, recommends, premiere_world_public, premiere_country_public
            ]
        """
        return self._fire_method('getFilmInfoFull [' + str(film_id) + ']')

    def get_film_description(self, film_id):
        raise NotImplementedError('Method is not yet implemented')

    def get_film_images(self, film_id):
        raise NotImplementedError('Method is not yet implemented')

    def get_film_persons(self, film_id):
        raise NotImplementedError('Method is not yet implemented')

    def get_film_review(self, film_id):
        raise NotImplementedError('Method is not yet implemented')

    def get_film_videos(self, film_id):
        raise NotImplementedError('Method is not yet implemented')

    def get_films_info_short(self, film_ids):
        raise NotImplementedError('Method is not yet implemented')

    def _prepare(self, method):
        """ Prepare data for request """

        md5 = hashlib.md5()

        signature = method + self._config.app_id + self._config.app_key
        md5.update(signature.encode('utf-8'))
        signature = self._config.api_version + ',' + md5.hexdigest()

        params = "version=" + urllib.parse.quote(self._config.api_version) + \
             "&appId=" + urllib.parse.quote(self._config.app_id) + \
             "&methods=" + urllib.parse.quote(method) + \
             "&signature=" + signature

        target_url = self._config.api_host + params

        return target_url, params

    def _fire_method(self, method):
        """ Make a request """

        target_url, _ = self._prepare(method + '\n')

        response = self._session.get(target_url, headers=self._request_headers)

        return self._parse_content(response.content)

    @staticmethod
    def _parse_content(content):
        """ Parse raw response's content """

        if isinstance(content, bytes):
            content = str(content.decode('utf-8'))
        content = content.replace("\\n", "\n")

        content = content.splitlines()[1]

        content = re.sub(r"^(\[.*\])[^\]]*$", r"\1", content)
        content = content.replace("null", "None")

        if not re.match(r"^\[.*\]$", content):
            return str(content)

        return ast.literal_eval(content)
