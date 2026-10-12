# Use–Verify–Cite log

## Method and provenance

**Use:** Preserve the original [Codex draft](ai_docstring.py) and its
[generation provenance](ai_generation_provenance.md). It was generated from
signatures and a goal only, before reading the implementation. Its schemas and
behavior were expressly hypothetical.

**Verify:** Inspect [server.py](../server.py) and run focused offline probes with
inert handler instances, mocks, and in-memory state. Distinguish a decoded JSON
value from an accepted endpoint payload, an application state from an HTTP code,
and user confirmation from authentication.

**Cite:** Record the actual source symbol that supports each correction. Cite
symbols rather than line numbers that change when docstrings are edited. The
accepted, code-informed documentation is in `server.py`; the raw draft remains
unchanged for comparison.

No independent human manual-authoring run was performed, and neither actual
GPT-4 nor Claude was called. This is a Codex-generated draft and code-reviewed
Codex revision. A conventional artifact filename does not alter that provenance.

## Observed contract and behavior findings

| Finding | Use: preserved draft hypothesis | Verify: implementation evidence | Cite and accepted correction |
|---|---|---|---|
| UVC-01: invented request-field proposal | `action`, `session_id`, `text` describe a command. | The command path invokes `fields()` with an exact set: `session_id`, `transcript`, `intent`, `event`. The raw proposal is rejected with `RequestError` status `400`. | `Handler.dispatch`, `fields`: replace the speculative schema with the exact command and nested event fields. This is an incompatible contract hypothesis, not a ghost method. |
| UVC-02: invented approval-field proposal | Confirmation uses `confirmed`; the body action selects the operation. | The confirm/execute operation and action ID come from the path. Both bodies require exactly `session_id`, `payload_version`; each raw draft body is rejected with `400`. | `Handler.dispatch`: remove `action` and `confirmed`; carry the returned action ID and version into the correct path/body. |
| UVC-03: invented response-field proposal | Envelope contains `message`. | The method returns exactly the keys `status`, `user_message`, `correlation_id`. A direct offline call confirms those keys. | `Handler.envelope`: document the actual names and the prerequisite `self.correlation`. |
| UVC-04: wrong logging hypothesis | `log_message()` writes a default server log. | Its body is `pass`; a capture probe produces no stdout or stderr. | `Handler.log_message`: document suppressed logging and ignored arguments. |
| UVC-05: wrong parser responsibility and shape hypothesis | `parse_body()` reads the stream and rejects arrays/scalars. | It uses `self.request_bytes`, pre-read in `do_POST()`. With a JSON `[]` body, it returns `[]`; shape validation belongs to `fields()` during dispatch. | `Handler.parse_body`, `Handler.do_POST`, `fields`: document preconditions and return type `object`, not dictionary-only validation. |
| UVC-06: incomplete media/size contract | POST requests are assumed to use JSON; limits are unknown. | Two upload paths parse multipart into text/file fields. Declared size over 2 MiB yields `RequestError(413)`; wrong media yields `415`. | `Handler.parse_body`, `LIMIT`: describe multipart file records and size/media errors. |
| UVC-07: wrong protocol exception hypothesis | Validation may raise `ValueError`; missing approval may raise `PermissionError`. | Application validation uses `RequestError`. Execution before confirmation is a `409`; `do_POST()` translates `RequestError` and selected ordinary Python exceptions separately. Date parsing can still raise `ValueError`. | `RequestError`, `Handler.dispatch`, `Handler.do_POST`: describe exceptions at the correct layer; do not remove genuine base exceptions. |
| UVC-08: wrong bearer-failure code hypothesis | Failed authorization is hypothesized as `403`. | Missing/invalid fixed bearer produces `401`, confirmed with an in-memory `do_POST()` probe. The `403` header branch is an injected provider-permission simulation. | `Handler.do_POST`, `TOKEN`: distinguish fixed sandbox authentication from failure simulation. |
| UVC-09: unverified side effects and durability | Real Calendar changes and replay behavior are left unknown; memory-only state is hypothesized. | State is initialized in server dictionaries. First confirmed execution increments a local counter and appends history; retry of a succeeded action leaves both counts at one. There is no provider/network write in this branch. | `SandboxServer.__init__`, `Handler.dispatch`: confirm memory-only state and simulated, idempotent execution within the running server. Do not infer durable or cross-restart idempotency. |

These findings were observed in the draft and source. They must be reported as
**explicitly qualified assumptions that failed verification** where applicable.
Calling them unqualified hallucinations would erase the draft's disclosed
uncertainty. UVC-01 through UVC-03 are invented *contract proposals*, not invented
callable APIs. Their incompatibility still makes them unsuitable for final API
documentation or copy-and-run examples.

## Corrected, source-compatible Calendar example

This example uses the required synthetic domain: session `session_anu_01`, event
`Sprint 06 review`, starting at `2026-10-12 10:00+08:00` and ending at 10:30.
The fixture token is for this local sandbox. No Google authorization or real
Calendar write is implied.

```http
POST /v1/commands
Authorization: Bearer sprint05-local-sandbox
Content-Type: application/json
```

```json
{
  "session_id": "session_anu_01",
  "transcript": "Create Sprint 06 review at 10:00 in Ulaanbaatar.",
  "intent": "calendar.create",
  "event": {
    "title": "Sprint 06 review",
    "start": "2026-10-12T10:00+08:00",
    "end": "2026-10-12T10:30+08:00",
    "timezone": "Asia/Ulaanbaatar"
  }
}
```

Use the response's `action_id` in `/v1/actions/{action_id}/confirm`, then
`/v1/actions/{action_id}/execute`. Both requests use the same authorization/media
headers and this exact JSON body, using the response's `payload_version`:

```json
{"session_id": "session_anu_01", "payload_version": 1}
```

The status sequence is `proposed` → `confirmed` → `succeeded`. Those application
states are returned with HTTP `200` in this flow. Source: `Handler.dispatch` and
`Handler.envelope`. These payloads and a repeated execution were checked offline
against the actual dispatch method; this log does not claim a live provider run.

## Artificial reflection negative control

`Handler.cancel_action` is a separately seeded, deliberately nonexistent method
name for a reflection test. It was **not** generated by the preserved raw draft,
was **not** discovered naturally, and is **not** an observed hallucination.
The raw draft's seven declared method names exist in the implementation.

A reflection test can demonstrate that a fabricated reference is detected. It
cannot establish that a payload schema, return value, status code, authorization
rule, or persistence promise is correct. The contract probes and source review
above address those different questions. Any result for the seeded control must
remain separately labeled as an artificial negative control.

## Literature boundary

The [lab handout](<C:/Users/PDulg/Downloads/Sprint 06 Lab Instructions - GitLab & Code Documentation.pdf>)
requires a Use–Verify–Cite record and a reflection bonus in US-6.3 and UE-6.
It names Bhatti's five principles but does not supply the full textbook passage.
This log does not claim an independent textbook or peer audit. It also does not
claim a naturally generated ghost method merely to satisfy the exercise.
