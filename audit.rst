AI audit and provenance
=======================

The primary comparison class is ``server.Handler``. ``manual_docstring.py`` is
an implementation-verified reference prepared with assistant help. Its filename
matches the lab's requested artifact; it is not evidence of independent student
manual authorship.

``audit/ai_docstring.py`` preserves an unaudited, signature-only Codex draft.
``bhatti_audit_table.md`` compares its claims against the implementation using
Explained, Concise, Clear, Usable and Trustworthy. The corrected reference and
``audit/manual_vs_ai.diff`` make the changes reviewable.

No GPT-4 or Claude API was called. If the instructor requires those engines
literally, run the saved prompt with that engine and retain the unedited result
before repeating the audit. No human review, named-engine run or production
execution is asserted by this package.

``tests/test_ai_hallucinations.py`` checks actual referenced symbols through
reflection and rejects a clearly labelled seeded ghost API. A seeded negative
control is separate from an organically observed AI hallucination.
