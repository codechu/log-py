# Security policy

`codechu-log` is a pure-stdlib structured logging library. It writes
to files and stderr; it does not open sockets, spawn processes, or
deserialize untrusted input. The attack surface is intentionally
small.

## Supported versions

| Version | Supported |
|---|:---:|
| `main` branch | ✅ |
| Latest minor release (0.x) | ✅ |
| Older releases | ❌ |

Pre-1.0.0 — only the latest minor receives security fixes.

## Reporting a vulnerability

### Preferred path — GitHub Security Advisory (private)

Open a **private** advisory at
[github.com/codechu/log-py/security/advisories/new](https://github.com/codechu/log-py/security/advisories/new).

### Alternative — Email

Write to `security@codechu.com`.

## Scope — what to report

**In scope:**

- A redaction key that fails to mask its value in either formatter.
- Log injection: a field value that breaks the JSON line boundary or
  the text format contract.
- Resource exhaustion: rotation failing to bound disk usage under
  documented `max_bytes` / `backup_count`.

**Out of scope:**

- Misuse: passing user-controlled data as the `name` of a logger or as
  a format string.
- The contents of log files themselves — securing the filesystem is
  the deploying application's responsibility.

## Process

Reports are reviewed on a best-effort basis — no fixed SLA. We aim
for coordinated disclosure within **90 days** of the report.

Public disclosure is coordinated after the fix is released.

## Public disclosure

Once a confirmed fix is released:

- A summary is added to the CHANGELOG under the `### Security`
  category.
- A GitHub Security Advisory is published.
- If a CVE was assigned, its number is referenced.
