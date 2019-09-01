# -*- coding: utf-8 -*-
""" Test for FilmwebAPI class """

import pytest
import requests
from filmweb_api import FilmwebApi
from filmweb_api.exceptions import LoginFailedException, WrongArgumentException

API_HOST = 'https://ssl.filmweb.pl/api'


def test_logout(mocker):
    """ Logout test """

    request_session = requests.session()
    mocker.patch.object(request_session.cookies, 'clear')

    sut = FilmwebApi('test_username', 'test_password', session_service=request_session)
    sut.logout()

    request_session.cookies.clear.assert_called_once()


def _login(sut, requests_mock):
    requests_mock.post(
        API_HOST + '?version=1.0&appId=android&methods=login%20%5B%22test_username%22%2C%20%22test_password%22%2C%201%5D%0A&signature=1.0,cc93095163a83e913c8346a734f9ddc8',
        text='ok\'b\n["test_username", "avatar.gif", "John Smith", 8889, "M"]',
        cookies={'_art_userid': 1231432523})

    sut.login()


def test_login(requests_mock):
    """ Login test - success """

    sut = FilmwebApi('test_username', 'test_password')

    _login(sut, requests_mock)

    assert sut.is_logged_in() is True


def test_login_failed(requests_mock):
    """ Login test - failure """

    requests_mock.post(API_HOST + '?version=1.0&appId=android&methods=login%20%5B%22test_username%22%2C%20%22test_password%22%2C%201%5D%0A&signature=1.0,cc93095163a83e913c8346a734f9ddc8',
                       text='ok\'b\n20, BadCredentials',
                       cookies={})

    sut = FilmwebApi('test_username', 'test_password')

    with pytest.raises(LoginFailedException):
        sut.login()


@pytest.mark.parametrize("username, password", [
    (None, None),
    ('some_username', None),
    (None, 'some_password'),
])
def test_login_no_credentials(username, password):
    sut = FilmwebApi(username, password)

    with pytest.raises(WrongArgumentException):
        sut.login()


def test_get_user_films_want_to_see(requests_mock):
    sut = FilmwebApi('test_username', 'test_password')

    _login(sut, requests_mock)

    expected_result = [1567198086181,[663821,1403959174000,5,0],[756,1397549920000,5,0]]

    requests_mock.get(
        API_HOST + '?version=1.0&appId=android&methods=getUserFilmsWantToSee%20%5B8889%2C%201%5D%0A&signature=1.0,d43b89bb43a4fea3be7921e8783b4856',
        text='ok\'b\n[1567198086181,[663821,1403959174000,5,0],[756,1397549920000,5,0]] s\n',
        cookies={})

    films = sut.get_user_films_want_to_see()

    assert expected_result == films
