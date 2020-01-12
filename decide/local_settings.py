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
    'authentication': 'http://articuno-census-heroku1.herokuapp.com/',
    'base': 'http://articuno-census-heroku1.herokuapp.com/',
    'booth': 'http://articuno-census-heroku1.herokuapp.com/',
    'census': 'http://articuno-census-heroku1.herokuapp.com/',
    'mixnet': 'http://articuno-census-heroku1.herokuapp.com/',
    'postproc': 'http://articuno-census-heroku1.herokuapp.com/',
    'store': 'http://articuno-census-heroku1.herokuapp.com/',
    'visualizer': 'http://articuno-census-heroku1.herokuapp.com/',
    'voting': 'http://articuno-census-heroku1.herokuapp.com/',
}

BASEURL = 'http://articuno-census-heroku1.herokuapp.com/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'decide',
        'HOST': '127.0.0.1',
	'PASSWORD': 'decide',
        'PORT': '5432',
    }
}

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256
