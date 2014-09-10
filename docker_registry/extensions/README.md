# WARNING 1: this is experimental and subject to break
# WARNING 2: installing and running third-party extensions present a security risk. Use caution.

# docker-registry extensions

You can further extend the registry behavior by authoring specially crafted python packages and listening to signals.

## Scaffolding

1. Start a new package (named `foo`)
3. Create folders `docker-registry` and `docker-registry/extensions` in your package 
4. Add the files `docker-registry/__init__.py` and `docker-registry/extensions/__init__.py` with the following content:

```
# -*- coding: utf-8 -*-
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)
```

5. create your extension main file `docker-registry/extensions/foo.py`
6. create a setup.py for your package (and then call `python setup.py develop`):

```
setuptools.setup(
    namespace_packages=['docker-registry', 'docker-registry.extensions'],
    packages=['docker-registry', 'docker-registry.extensions'],
```

6. run your registry with DEBUG=true so that gunicorn reloads on file change

## Installing

As soon as your python package is installed on the system, your code will get executed.
The main communication API with the registry is through signals (see below).

As far as your users are concerned, all they have to do should be `pip install my-foo-package` (you may require them to add some specific configuration, including to explicitely enable your extension - see below).

That's it.


## API

This very simple example will print when a tag is created:

```
from docker_registry.lib import signals


def receiver():
    print('I am a tag creation receiver')

signals.namespace.signal('tag-created').connect(receiver)

```

You can access configuration options through the config API:

```
from docker_registry.lib import config

myconfig = config.load()
```

That will give you what the user specified in its configuration file under the YAML key `extensions.foo` (where `foo` corresponds to `foo.py`), like for example:

```
extensions:
    foo:
        setting: _env:EXTENSION_FOO_SETTING
```

For convenience, you may also use the following APIs from core:

```
from docker_registry.core import compat
from docker_registry.core import exceptions
```

(see the code...)

## Versioning and compatibility

Right now there is no versioning strategy (save on core), although we will do our best not to break the API for `signals` and `config`.

Any other docker_registry API should be considered private / unstable, and as a responsible extension author, you should think twice before using said internals...

## Packaging and distribution

The prefered way to package is through pypi.

Your package must depend on `docker-registry-core>=2,<3`

