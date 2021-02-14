try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

from . import config

def res(rel_path):
    return urljoin(config.get('res.path', '/'), rel_path)
