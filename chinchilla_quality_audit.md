# Documentation quality audit: six operational checks

## Attribution boundary

The [Sprint 06 lab handout](<C:/Users/PDulg/Downloads/Sprint 06 Lab Instructions - GitLab & Code Documentation.pdf>)
names Chinchilla's “six principles” but does **not enumerate their labels**. In
US-6.1 it asks for descriptions, parameters, return types, possible errors,
consistent domain examples, and an explanation for internal exclusions. Its
consistent-example requirement cites Chinchilla Chapter 7, pages 89–90.

The actual textbook passage was not available for this audit. Accordingly, the
following are **six operational checks derived from the handout**, not asserted
verbatim Chinchilla principle names or a verified account of those textbook
pages. Verification against the primary textbook remains pending. The page
reference is the handout's secondary attribution.

## Scope and evidence standard

This review inspected [server.py](server.py) and its seven `Handler` methods, then
checked the surrounding module's project-declared public documentation. The
comparison baseline is the preserved [signatures-only draft](audit/ai_docstring.py).
Source citations name symbols rather than unstable line numbers.

“Addressed” means the inspected code-informed documentation meets the specified
local check. It does not mean a human peer approved it, a textbook author endorsed
it, a public GitLab pipeline ran, or a production integration was tested. No
numeric quality score is assigned. The authorship limitation is explicit: both
the draft and source-informed revision are Codex artifacts; independent human
manual authoring and actual GPT-4/Claude runs were not performed.

## Six-check matrix

| Operational check derived from the handout | Raw draft assessment | Inspected code-informed documentation and source evidence | Qualitative result |
|---|---|---|---|
| **1. Describe purpose and operating boundary** | States the Calendar flow but cannot establish real versus simulated effects, constructor lifecycle, or inherited static serving. | Module and `Handler` docs explain local simulation, static `public` serving, inherited connection processing, and memory-only state. `SandboxServer` docs identify shared state and POST locking. | **Addressed for the local sandbox.** No real Google/OAuth/AI or durable persistence is implied. |
| **2. Specify parameters and accepted data** | Speculative `action`, `text`, and `confirmed` fields would fail exact-field validation. Media and parser inputs are uncertain. | `Handler.dispatch` gives command fields, nested event fields, `calendar.create`, matching session/version requirements, and upload records. `Handler.parse_body` documents pre-read `request_bytes`, JSON versus multipart, and length checks. `fields`/`text_fields` distinguish shape and text validation. | **Addressed for the selected API.** Offline probes rejected raw schemas with `400` and accepted the corrected Calendar schema. |
| **3. State return types and response structures** | Hypothesizes `message` in the response and dictionary-only parsing. | `Handler.envelope` names `status`, `user_message`, `correlation_id`; `parse_body` returns any JSON value or a multipart dictionary; `dispatch` returns an HTTP code/response pair; response writers return `None`. The docs distinguish endpoint-specific upload/subscription results from the common envelope. | **Addressed.** Envelope keys and JSON-array parsing were checked directly; symbol existence alone would not verify these structures. |
| **4. Document errors, prerequisites, and side effects** | Exception classes and authorization codes are speculative; pending approval and real effects are unresolved. | `RequestError` and method `Raises` sections distinguish protocol failures from ordinary Python exceptions. `do_POST` documents fixed bearer checking (`401` on missing/invalid token), injected failures, capped reads, error conversion, and lock ownership. `dispatch` documents confirmation/version conflicts and one simulated write on first execution. | **Addressed within source behavior.** Helper calls can bypass transport authentication/locking; this is disclosed. No general security assurance or cross-restart durability is claimed. |
| **5. Use consistent, source-compatible domain examples** | Reuses the requested session/title/time, but examples use incompatible hypothetical contracts and have no executable skeleton behavior. | The corrected Calendar example uses `session_anu_01`, `Sprint 06 review`, and `2026-10-12T10:00+08:00` with a 10:30 end and `Asia/Ulaanbaatar`. `Handler.dispatch` demonstrates proposal, confirmation, execution, and retry using initialized in-memory state. Individual helpers use the same session or event where relevant. | **Addressed for the assistant domain.** Source-backed examples replace invented fields. Separate Corg.ly fixture routes are separate API exercises; they are not presented as Calendar event data. |
| **6. Cover the declared public surface in structured documentation** | Covers the supplied class and seven methods only; signatures alone cannot establish the whole module's public inventory. | The module has documentation; all three project-declared classes, their nine methods including constructors, and both top-level functions have structured docstrings (14 declared public classes/callables). Constants `ROOT`, `TOKEN`, `LIMIT` have typed attribute comments. `Handler` documents inherited behavior without pretending to re-document every standard-library inherited member. | **Addressed for source documentation coverage.** Render/build results must be taken from actual build logs, not inferred here. No project-declared internal helper was silently excluded from the checked module. |

## Specific improvements and verification

The largest usability correction was replacing `action`/`text`/`confirmed` with
the implemented field sets and path-based action selection. The clearest return
contract correction was `message` → `user_message` plus `correlation_id`.
Responsibility was also corrected: `do_POST` reads and authenticates;
`parse_body` decodes the pre-read bytes; `dispatch` validates endpoint data and
mutates only local fixtures. These changes are traceable to `fields`,
`Handler.do_POST`, `Handler.parse_body`, `Handler.dispatch`, and
`Handler.envelope` rather than inferred from method names.

Focused offline checks on 2026-10-12 established:

- All three speculative draft request bodies were rejected with `RequestError`
  status `400` on their corresponding real paths.
- `envelope()` used the three documented real keys, `parse_body()` accepted JSON
  `[]`, and `log_message()` emitted no stdout/stderr.
- A corrected Calendar request progressed through `proposed`, `confirmed`, and
  `succeeded`; repeating execution kept one simulated provider write and one
  history record.
- A missing sandbox bearer yielded `401` through `do_POST()` with mocked I/O.

These checks used mocks and isolated state. They support the local documentation
claims above and do not establish a deployed system, real Calendar execution, or
all possible malformed-input behavior. The [Bhatti audit](bhatti_audit_table.md)
and [Use–Verify–Cite log](audit/use_verify_cite.md) retain detailed corrections.

## Remaining academic verification

Obtain the primary Chinchilla text and confirm its exact six labels and relevant
passage before claiming direct compliance with those named principles. Obtain
any required human manual-authoring/peer-review evidence and actual specified
model runs separately; this agent audit cannot substitute invented provenance.
The current six checks are a transparent, handout-derived operational review.
