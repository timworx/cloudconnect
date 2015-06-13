try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Python Cloudflare Wrapper',
    'author': 'Tim Sherwood',
    'url': '',
    'download_url': '',
    'author_email': '',
    'version': '0.1',
    'install_requires': ['nose', 'requests', 'tldextract'],
    'packages': ['cloudconnect'],
    'scripts': [],
    'name': 'CloudConnect'
}

setup(**config)