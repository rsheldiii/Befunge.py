try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Befunge.py',
    'author': 'Robert Sheldon',
    'url': 'www.github.com/rsheldiii/Benfunge.py',
    'download_url': 'www.github.com/rsheldiii/Benfunge.py',
    'author_email': 'rsheldiii@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['befunge'],
    'scripts': [],
    'name': 'Befunge.py'
}

setup(**config)
