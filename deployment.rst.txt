GitLab CI and Pages
===================

The supplied URL is a GitHub repository. GitHub does not execute
``.gitlab-ci.yml``. Import or push this source to a GitLab project to satisfy the
lab's GitLab deployment requirement.

The verification job runs tests, coverage checks, doctests and a strict HTML
build on branch pushes and merge requests. Only the default branch publishes
``public`` through the modern job-level ``pages.publish`` setting. A verification
failure blocks deployment. The existing Swagger and Redoc files remain in
``public`` alongside the new Sphinx reference.

After pushing, validate the configuration in GitLab's CI Lint, wait for a green
pipeline, then open Deploy > Pages and copy the actual URL into
``GITLAB_PUBLISH.md``. Do not infer the URL from a username: GitLab can assign a
unique Pages domain. Check it in a signed-out browser if public access is
required. Pages hosts static reference files, not the Python sandbox.

Sources checked on 12 October 2026:

* `GitLab CI YAML: pages <https://docs.gitlab.com/ci/yaml/#pages>`_
* `GitLab Pages settings <https://docs.gitlab.com/user/project/pages/introduction/>`_
* `GitLab deployment tutorial <https://docs.gitlab.com/user/project/pages/getting_started/pages_ui/>`_
* `Sphinx build command <https://www.sphinx-doc.org/en/master/man/sphinx-build.html>`_

Local build logs verify local results only. A real GitLab job URL and Pages URL
remain pending until a deployment actually occurs.
