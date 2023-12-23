from memcache import Client

from app.settings import settings


def get_store() -> Client:
    return Client([settings.memcached_server], debug=1)
