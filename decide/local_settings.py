ALLOWED_HOSTS = ["*"]

# Modules in use, commented modules that you won't use
MODULES = [
    'authentication',
    'base',
    'booth',
    'census',
    'mixnet',
    'postproc',
    'store',
    'visualizer',
    'voting',
]

BASEURL = 'https://articuno-census-heroku.herokuapp.com'

APIS = {
    'authentication': 'https://articuno-census-heroku.herokuapp.com',
    'base': 'https://articuno-census-heroku.herokuapp.com',
    'booth': 'https://articuno-census-heroku.herokuapp.com',
    'census': 'https://articuno-census-heroku.herokuapp.com',
    'mixnet': 'https://articuno-census-heroku.herokuapp.com',
    'postproc': 'https://articuno-census-heroku.herokuapp.com',
    'store': 'https://articuno-census-heroku.herokuapp.com',
    'visualizer': 'https://articuno-census-heroku.herokuapp.com',
    'voting': 'https://articuno-census-heroku.herokuapp.com',
}



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256
