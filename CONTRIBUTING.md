# Contributing to DashyNMS

Bug reports, accessibility reports and ideas are welcome. Start in the affected
repository and check its CONTRIBUTING.md before preparing a code change. Open
an issue first to agree the scope; acceptance and review depend on the change
and the repository's contribution policy.

Use the bug and feature forms. Include the version, platform and steps to
reproduce a problem. Use synthetic data such as `example.net` and documentation
IP addresses. Remove credentials, customer names and identifiable network details
from text, logs and screenshots. Report vulnerabilities privately under
[SECURITY.md](SECURITY.md), and follow the [code of conduct](CODE_OF_CONDUCT.md).

Work on a branch into `main`, with one issue per PR. Use a title such as
`fix(alerts): preserve the selected filter`; the complete convention and scopes
are in each repository's developer guide. Describe the resulting behaviour,
validation and affected consumers. Keep commits, PRs and release notes free of
AI attribution and co-author lines. Maintainers normally squash-merge PRs.

Run the affected build, test and security checks. State which passed and which
were unavailable. Add release notes when users or consumers would notice the
change. Mobile's What's New is a curated set of highlights. Preserve third-party
licences, provenance and immutable published versions. Project-owned code and
assets use MIT; upstream terms and trademark rights remain applicable.

For this shared repository, install `requirements-security.txt`, run
`python -m unittest discover -s scripts/tests -v`, and run the checks described
in [Maintaining repository standards](docs/REPOSITORY-STANDARDS.md). Change the
canonical scripts and templates here before distributing a new version to the
application repositories.

Every PR needs an existing issue describing the bug or intended change, including
small documentation, dependency and CI updates. Create or find the issue before
opening the PR. Use a closing reference for completed work and a non-closing
reference for partial work.
