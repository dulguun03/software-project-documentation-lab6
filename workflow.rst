Contract and implementation boundaries
======================================

``POST /v1/commands`` creates a proposed action. Confirmation and execution are
separate requests at ``/v1/actions/{id}/confirm`` and
``/v1/actions/{id}/execute``. Both require the same session and payload version.
Execution without confirmation is rejected with HTTP 409. Repeated execution
of a succeeded action returns the same simulated resource ID and does not add
another simulated write or history entry.

The server serializes POST handling with a shared lock. ``dispatch`` itself
does not acquire the lock or authenticate callers; ``do_POST`` supplies that
context. Directly calling ``dispatch`` is useful for isolated tests, but it
must not be described as an authenticated HTTP entry point.

State is held in dictionaries and is lost on restart. Contacts are a single
fixture. The webhook endpoint validates and echoes a subscription; it does not
persist a subscription or deliver callbacks. The bark endpoint checks the WAV
header and returns a deterministic simulated result.

The request body limit is 2 MiB. The POST handler maps known request errors to
JSON error responses. It also maps uncaught malformed-value errors to 400 and
unexpected errors to 500. Documentation examples must distinguish a helper's
Python exception from the HTTP response produced by ``do_POST``.

The Sprint 05 OpenAPI files remain under ``docs/openapi``. They describe the
HTTP interface; this reference documents the Python symbols implementing it.
