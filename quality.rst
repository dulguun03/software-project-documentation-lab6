Documentation quality and technical debt
=========================================

Google-style docstrings use descriptions, typed parameters, return values,
errors and runnable examples. Napoleon converts them to reStructuredText for
autodoc. Examples use one domain schema, with synthetic local data and no
provider calls. ``-W`` makes warnings fail the build; ``-n`` checks unresolved
references. A separate doctest build executes examples.

``chinchilla_quality_audit.md`` records six operational quality checks and the
limits of their attribution. The supplied handout cites Chinchilla Chapter 7
but does not enumerate its six principles. The textbook passage was not
provided; this package does not invent its exact wording or claim a page-level
reading. Replace the operational labels with verified course labels if needed.

``technical_debt_audit.md`` records a token-based scan of authored Python
comments. Vendored assets and generated output are excluded. Unresolved markers
must reference a real GitLab issue ID; fabricated IDs are not accepted.

The Calendar sample regression found in the supplied repository was resolved:
its commented-out confirmation request prevented the advertised workflow from
executing. The original unconfirmed-execution rejection test remains in place.
