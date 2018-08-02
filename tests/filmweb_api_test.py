# -*- coding: utf-8 -*-
""" Test for FilmwebAPI class """

import pytest
import requests
from src.filmweb_api import FilmwebApi
from src.exceptions import LoginFailedException

API_HOST = 'https://ssl.filmweb.pl/api'


def test_logout(mocker):
    """ Logout test """

    request_session = requests.session()
    mocker.patch.object(request_session.cookies, 'clear')

    sut = FilmwebApi('test_username', 'test_password', session_service=request_session)
    sut.logout()

    request_session.cookies.clear.assert_called_once()


def test_login(requests_mock):
    """ Login test - success """

    requests_mock.post(API_HOST + '?version=1.0&appId=android&methods=login%20%5B%22test_username%22%2C%20%22test_password%22%2C%201%5D%0A&signature=1.0,cc93095163a83e913c8346a734f9ddc8',
                       text='ok\'b\n["test_username", "avatar.gif", "John Smith", 8889, "M"]',
                       cookies={'_art_userid': 1231432523})

    sut = FilmwebApi('test_username', 'test_password')
    sut.login()

    assert sut.is_logged_in() is True


def test_login_failed(requests_mock):
    """ Login test - failure """

    requests_mock.post(API_HOST + '?version=1.0&appId=android&methods=login%20%5B%22test_username%22%2C%20%22test_password%22%2C%201%5D%0A&signature=1.0,cc93095163a83e913c8346a734f9ddc8',
                       text='ok\'b\n20, BadCredentials',
                       cookies={})

    sut = FilmwebApi('test_username', 'test_password')

    with pytest.raises(LoginFailedException):
        sut.login()
