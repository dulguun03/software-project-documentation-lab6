Python API reference
====================

Scope
-----

All locally declared public classes, functions and methods in ``server.py`` and
the shared ``samples/client.py`` transport are included. Constructors are
included in their class reference. Inherited standard-library methods are
outside this project's authored API. Test helpers, build scripts, configuration,
and executable-only sample modules are internal tools, not supported imports.
The sample modules send HTTP requests at import time, so autodoc imports only
their shared client. Vendored Swagger JavaScript belongs to its upstream API.

Sandbox server
--------------

.. automodule:: server
   :members:
   :undoc-members:
   :exclude-members: ROOT

.. autodata:: server.ROOT
   :no-value:

Sample transport
----------------

.. automodule:: client
   :members:
   :undoc-members:
