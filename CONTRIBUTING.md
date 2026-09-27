# Contributing to sms-call-flood-tester

Thanks for wanting to help the flood-tester grow. This repo is a community
project for load-testing SMS and voice gateways you own or are authorized
to test. Contributions of every size are welcome.

## Ground rules

- One feature per pull request. Keep diffs reviewable.
- Every new handler in `src/flood/handlers/` must ship with a matching
  test under `tests/handlers/`.
- Do not commit real target lists, carrier credentials, or session dumps.
- Use the vocabulary of the project. A "flood" is a flood. Don't rename
  it to something softer — it breaks grep and it breaks discoverability.

## Getting set up

```bash
git clone https://github.com/<owner>/sms-call-flood-tester
cd sms-call-flood-tester
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

Run the test suite before opening a PR:

```bash
pytest -q
```

## Style

- Python 3.12+, `ruff` and `black` clean.
- Type hints on every public function. `mypy --strict` on `src/flood/core`.
- No bare `except:`. Catch the specific exception, log it, decide.
- Logging through `flood.utils.logging`, never `print`.

## Adding a new transport

1. Drop a module in `src/flood/services/`.
2. Subclass `flood.core.transport.BaseTransport`.
3. Register it in `src/flood/config/registry.py`.
4. Add a fixture and a test.

## Reporting bugs

Open an issue with: OS build, Python version, the exact command, and the
last 50 lines of `logs/flood.log`. Redact phone numbers.

## Code of conduct

Be a decent human. Roast code, not people.