SECRET_KEY = '3y8m!1yt0cehz4bon*5)@_a0tk8u3axr$zsn#_ggd9f&bx*po1'

ALLOWED_HOSTS = ['www.example.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test',
        'USER': 'test',
        'PASSWORD': 'psw123456',
        'HOST': 'localhost', # Set to empty string for localhost.
        'PORT': '5432', # Set to empty string for default.
        }
}

DEBUG = True