# Contributing to Inertia-Rebellion

Thank you for your interest in contributing.
This repository is intentionally structured to prioritize **clarity, falsifiability,
and methodological rigor** over speculation or advocacy.

Contributions are welcome from supporters, skeptics, and critics alike.

---

## Project Philosophy

This project is guided by three core principles:

1. **Methodology before interpretation**  
   Numerical and experimental tools must be correct before any physical claims
   are considered.

2. **Falsification over confirmation**  
   Contributions that stress-test assumptions, expose failure modes, or
   demonstrate null results are valued equally with positive results.

3. **Explicit scope control**  
   No contribution should imply new physics unless explicitly labeled as
   speculative and clearly separated from validated analysis.

---

## What This Repository Is — and Is Not

### This repository **is**:

- A platform for **numerical validation** of analysis pipelines
- A space for **transparent falsification and null testing**
- An environment for **independent replication and critique**
- A pre-hardware discipline checkpoint

### This repository **is not**:

- A proof of new physics
- A claim of anisotropic inertia
- A place for unsupported theoretical speculation
- A substitute for experimental validation

---

## Types of Contributions Welcome

We explicitly encourage:

- Improvements to numerical stability or performance
- Additional null tests or falsification checks
- Alternative analysis pipelines for comparison
- Independent reproductions of existing results
- Documentation clarity improvements
- Identification of bugs, edge cases, or hidden assumptions

Contributions that **reduce confidence** for well-founded reasons
are considered successful contributions.

---

## Contributions That Will Be Rejected

To maintain scientific discipline, the following will not be accepted:

- Claims of discovery based solely on simulations
- Reinterpretation of results beyond stated scope
- Removal or weakening of falsification tests
- Changes that obscure assumptions or hide failure modes
- Overfitting analysis to achieve higher SNR
- Introducing speculative physics into validated pipelines

If you are unsure whether a contribution fits, open an issue first.

---

## Contribution Workflow

1. **Fork** the repository
2. Create a **feature branch** (`feature/description`)
3. Make your changes with clear, minimal commits
4. Add or update tests where applicable
5. Update documentation if behavior or interpretation changes
6. Open a **pull request** with a clear explanation of:
   - what was changed
   - why it was changed
   - what assumptions are affected

---

## Documentation Standards

- Mathematical symbols must be defined on first use
- Units must be explicitly stated
- All assumptions must be documented
- README, methods, and code must remain consistent

If a change modifies interpretation, it must be reflected in:
- `README.md`
- `methods.md`
- `discussions.md` (if applicable)

---

## Code Standards

- Python 3.x only
- Deterministic behavior unless randomness is intentional and seeded
- Explicit configuration via parameters or config files
- No hidden “magic numbers”
- No silent exception handling

Numerical shortcuts must be justified in comments or documentation.

---

## Falsification Requirements

Any contribution that introduces:
- a new signal model,
- a new extraction method,
- or a new decision metric

**must include at least one falsification test**, such as:
- wrong-frequency recovery
- null injection
- phase randomization
- parameter scrambling

A method that cannot fail cleanly is not acceptable.

---

## Review Criteria

Pull requests are evaluated on:

- Clarity and transparency
- Consistency with stated scope
- Presence of falsification checks
- Reproducibility
- Scientific restraint

Rejection is not a judgment of intent — it is enforcement of scope.

---

## Reporting Issues

Bug reports and critiques are encouraged.

Please include:
- expected behavior
- observed behavior
- configuration or parameters used
- minimal reproducible examples when possible

Ambiguous or speculative issues may be redirected to discussion.

---

## Attribution and Credit

Contributors retain credit for their work.
Significant contributions will be acknowledged in documentation
or release notes.

No contribution implies endorsement of any physical interpretation.

---

## Final Note

This project values **intellectual honesty over optimism**.

If your contribution makes the experiment harder, more constrained,
or more likely to fail for good reasons — it is a success.

Thank you for helping keep this work disciplined and falsifiable.
