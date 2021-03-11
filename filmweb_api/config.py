
DEFAULT_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'
DEFAULT_API_HOST = 'https://ssl.filmweb.pl/api?'
DEFAULT_API_VERSION = '1.0'
DEFAULT_APP_ID = 'android'
DEFAULT_APP_KEY = 'qjcGhW2JnvGT9dfCt3uT_jozR3s'


class Config:
    user_agent = DEFAULT_USER_AGENT
    api_host = DEFAULT_API_HOST
    api_version = DEFAULT_API_VERSION
    app_id = DEFAULT_APP_ID
    app_key = DEFAULT_APP_KEY
    username = None
    password = None

    def __init__(self, settings=None):
        if isinstance(settings, dict):
            for key, value in settings.items():
                if not hasattr(self, key):
                    raise Exception('Config has no attribute named: %s' % key)
                setattr(self, key, value)
