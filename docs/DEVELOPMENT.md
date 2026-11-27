# Developing repository standards

Use Python 3.12 or newer. Setup, security checks and distribution instructions are
in [Repository standards](REPOSITORY-STANDARDS.md).

## Commits, pull requests and issues

Every PR needs an issue describing the bug or intended change before the PR is
opened. Use `type(scope): lower-case result`, with optional scopes `ci`, `deps`,
`docs` and `security`. Types are `feat`, `fix`, `perf`, `refactor`, `docs`, `test`,
`build`, `ci`, `chore` and `revert`. Use a breaking `!` when consumer action is
required. Keep titles within 72 characters, without a final full stop or issue
number. Authenticated Dependabot's generated dependency titles have a narrow exception
for capitalisation and length.

## Release notes

This repository distributes reviewed source commits rather than product
releases. Describe consumer impact and validation in the issue and PR. Each
consumer locks the source revision and hashes; published consumer versions stay
immutable.
