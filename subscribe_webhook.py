"""Register an illustrative HTTPS callback for Einstein's pet activity.

Run ``python samples/subscribe_webhook.py`` after starting the local sandbox.
Importing this script also executes its top-level POST request; it is an
executable demonstration, not a reusable Python API. It defines no public
functions or classes, so only this module-level demonstration is documented.
The sandbox records the subscription but never sends outbound callbacks to
``https://example.org/corgly/pet-activity``. The pet fixture is ``corgi_98231``.
"""
from client import post

subscription = {
    "pet_id": "corgi_98231",
    "callback_url": "https://example.org/corgly/pet-activity",
    "events": ["pet.activity.detected"],
}
post("/webhooks/subscribe", subscription)
