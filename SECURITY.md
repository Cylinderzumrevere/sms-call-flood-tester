# Security Policy

## Supported versions

| Version | Supported          |
| ------- | ------------------ |
| 0.6.x   | :white_check_mark: |
| 0.5.x   | :white_check_mark: |
| < 0.5   | :x:                |

## Reporting a vulnerability

Do not open a public issue for security problems. Email
`security@sms-call-flood-tester.dev` with:

- A description of the issue.
- Steps to reproduce.
- The affected version and platform.
- Whether the issue is exploitable without local access.

You'll get an acknowledgement within 72 hours and a fix or a mitigation
plan within 14 days.

## Scope

The flood-tester is a load-generation tool. It is meant to be pointed at
gateways **you own or have written authorization to test**. Running it
against a third party's SMS or voice infrastructure without permission is
abuse, is illegal in most jurisdictions, and is not a supported use case.

## Known limitations

- The HTTP transport does not verify TLS by default when `--insecure` is
  passed. Don't use `--insecure` on untrusted networks.
- Proxy credentials are stored in plaintext in `config.toml` unless you
  set `FLOOD_PROXY_KEY` and use the encrypted store.
- The SIP transport is experimental. Do not point it at production
  carriers.

## Hardening checklist for operators

- Run inside a VM or container with egress restricted to the target.
- Rotate proxy pools every session.
- Keep `logs/` off any synced drive.
- Never ship `config.toml` with real credentials to a public fork.