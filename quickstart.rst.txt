Run the sandbox and build the reference
=======================================

Use Python 3.12. The sandbox itself uses only the standard library.
Run from the repository root:

.. code-block:: console

   python server.py

In another terminal:

.. code-block:: console

   python samples/assistant_workflow.py
   python samples/upload_photo.py
   python samples/translate_bark.py
   python samples/subscribe_webhook.py

The Calendar example confirms its pre-reviewed fixture before simulated
execution. A product UI must separately obtain the user's confirmation.
The media fixtures are synthetic; the bark response is a fixed demonstration.

The original Sprint 05 HTTP reference remains at
``http://127.0.0.1:8080/swagger/``, ``/redoc.html`` and ``/corgly-redoc.html``.
Use the public demo bearer value ``sprint05-local-sandbox`` in Swagger Authorize.
It is not a Google token or a production authentication mechanism.

Build the API documentation:

.. code-block:: console

   python -m pip install -r requirements-docs.txt
   python -m unittest discover -s tests -v
   python scripts/check_documentation.py
   python -m doctest server.py samples/client.py
   python -m sphinx -W --keep-going -n -b doctest docs/source .build/doctest
   python -m sphinx -W --keep-going -n -b html docs/source public

Open ``public/index.html`` after a successful build. The Sphinx build uses
built-in autodoc and napoleon extensions; no separate ``autodoc`` distribution
is needed. HTML generation does not start the application or call a provider.
