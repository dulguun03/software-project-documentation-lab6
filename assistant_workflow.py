"""Propose, confirm, and simulate the Sprint 06 review, then read its history.

Run ``python samples/assistant_workflow.py`` after starting the local sandbox.
Importing this script also executes all five top-level POST requests; it is an
executable demonstration, not a reusable Python API. It defines no public
functions or classes, so only this module-level demonstration is documented.
The fixture creates a simulated Calendar event on 12 October 2026 from 10:00
to 10:30 in ``Asia/Ulaanbaatar``. This fixture is pre-reviewed for the automated
demo; a real UI must ask the user before confirming the proposed action. The
sandbox simulates the provider write rather than contacting Google Calendar.
"""
from client import post

command = {
    "session_id": "session_anu_01",
    "transcript": "Schedule the Sprint 06 review on 12 October at 10 AM.",
    "intent": "calendar.create",
    "event": {"title": "Sprint 06 review", "start": "2026-10-12T10:00:00+08:00",
              "end": "2026-10-12T10:30:00+08:00", "timezone": "Asia/Ulaanbaatar"},
}
proposal = post("/commands", command)
action_id = proposal["action_id"]
confirmation = {"session_id": "session_anu_01", "payload_version": proposal["payload_version"]}
post(f"/actions/{action_id}/confirm", confirmation)
post(f"/actions/{action_id}/execute", confirmation)
post("/contacts/search", {"query": "Anu"})
post("/sessions/history", {"session_id": "session_anu_01"})
