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

APIS = {
    'authentication': 'https://egc-articuno-census.herokuapp.com/',
    'base': 'https://egc-articuno-census.herokuapp.com/',
    'booth': 'https://egc-articuno-census.herokuapp.com/',
    'census': 'https://egc-articuno-census.herokuapp.com/',
    'mixnet': 'https://egc-articuno-census.herokuapp.com/',
    'postproc': 'https://egc-articuno-census.herokuapp.com/',
    'store': 'https://egc-articuno-census.herokuapp.com/',
    'visualizer': 'https://egc-articuno-census.herokuapp.com/',
    'voting': 'https://egc-articuno-census.herokuapp.com/',
}

BASEURL = 'https://articuno-census-heroku1.herokuapp.com/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256
