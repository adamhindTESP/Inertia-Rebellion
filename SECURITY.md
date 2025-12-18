# Security Policy

## Scope

This repository contains research code, numerical simulations, and
documentation related to signal-processing validation and sensitivity analysis.

It does **not** contain:
- production systems
- deployed services
- authentication mechanisms
- sensitive personal data
- operational infrastructure

Security considerations here focus on **code integrity, reproducibility,
and responsible disclosure of issues** that could affect correctness or trust.

---

## Supported Versions

This project does not maintain long-term supported releases.
Security-related fixes are applied to the `main` branch.

Users are encouraged to pull the latest version before running or modifying
the code.

---

## What Constitutes a Security Issue

In the context of this repository, a security issue includes:

- Code execution vulnerabilities when running scripts as documented
- Dependency-related vulnerabilities that materially affect users
- Malicious code insertion or supply-chain compromise
- Tampering that could falsify results without clear indication
- Undocumented behavior that undermines reproducibility or auditability

Purely theoretical concerns without a plausible exploitation path
are generally treated as bugs or design discussions, not security issues.

---

## What Is *Not* a Security Issue

The following are **not** considered security issues:

- Disagreement with scientific assumptions or conclusions
- Claims that the modeled physics is incorrect
- Numerical instability that is documented or reproducible
- Performance limitations
- Requests for new features or enhancements

These should be reported via standard issues or pull requests.

---

## Reporting a Security Issue

If you believe you have found a security-related issue, please report it
responsibly.

**Preferred method:**
- Open a private communication with the repository maintainer

**If private contact is not available:**
- Open a GitHub issue labeled `security`
- Avoid publishing exploit details until triage is complete

Please include:
- A clear description of the issue
- Steps to reproduce
- Affected files or dependencies
- Potential impact on users or results

---

## Responsible Disclosure

We ask reporters to allow reasonable time for investigation and remediation
before public disclosure.

This project values transparency, but also prioritizes:
- preventing misuse
- protecting result integrity
- avoiding unnecessary alarm

---

## Dependency Management

Dependencies are intentionally minimal and widely used.
Users are encouraged to:

- Review dependency versions
- Use virtual environments
- Monitor upstream security advisories

No automated dependency scanning is currently enforced.

---

## Reproducibility and Integrity

Security in this project is closely tied to reproducibility.

Practices used to support integrity include:
- Explicit configuration files
- Deterministic behavior where feasible
- Metadata logging for all runs
- No hidden network access or telemetry

Any change that undermines these properties may be treated as a security concern.

---

## Enforcement

Security issues are handled by repository maintainers.
Actions may include:
- Code review and patching
- Temporary disabling of affected components
- Public advisories when appropriate

There is no bug bounty program.

---

## Final Note

This is a research repository, not a hardened production system.

The goal of this policy is to protect:
- the integrity of the code
- the credibility of the results
- and the trust of contributors and reviewers

Good-faith reporting is appreciated.
