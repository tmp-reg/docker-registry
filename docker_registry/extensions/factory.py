import pkgutil

import docker_registry.extensions


def boot(config=None):
    # Import all available extensions:
    for importer, modname, ispkg in pkgutil.iter_modules(
            docker_registry.extensions.__path__):
        if not 'docker_registry.extensions.%s' % modname == __name__:
            __import__('docker_registry.extensions.%s' % modname,
                       globals(), locals())  # noqa
