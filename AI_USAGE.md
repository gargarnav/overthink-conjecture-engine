# AI usage in this project

## 1. AI as a research component: the conjecture proposer

`src/overthink/conjecture/llm.py` defines a provider-agnostic proposer:

| Provider | What it is | Used so far |
|---|---|---|
| `mock` | deterministic toy proposals, for tests | tests only |
| `session` | an AI coding assistant working interactively, which reads a committed data packet and writes proposals as JSON | family H (`experiments/familyH/`) |
| `anthropic` | API provider, not configured (no API key) | never |

**Rules that every AI proposal follows:**

1. **Window only.** The proposer sees only a data packet built from the proposal window (`overthink llm-packet`). The packet's SHA-256 is committed first, and the session provider rejects proposals made for any other packet.
2. **Commit before test.** Proposals are committed before any falsification runs (family H: proposals `f9020d9`, tests `186d49f`).
3. **Machine-checkable.** Each proposal must be a claim in the whitelisted claim language (`conjecture/claims.py`). Malformed claims are rejected and reported.
4. **Counted only after checking.** A claim counts as *surviving* only if it holds on the proposal data *and* on at least 10× more data. It counts as *proved* only if a Lean proof compiles with standard axioms only (no `sorry`, no `native_decide`).
5. **Everything is reported,** including refuted and rejected proposals.

**Logging.** Each LLM run records in its `run.json` the provider, the model identifier, the packet SHA-256 (the prompt hash), approximate input tokens (characters / 4), output size, and API cost. No API has been called so far: total API spend is **$0**. Model identifiers are kept in the run records and the registry event log.

## 2. AI-assisted development

This repository (Python, Rust, Lean, documentation) was written with substantial help from an AI coding assistant, under the author's direction. Safeguards:

- tests (pytest, cargo test), type checking, and CI on every push;
- the Lean kernel for every claimed proof;
- falsification at 10× scale for every surviving conjecture;
- pre-registration (git tags) for blind experiments;
- independent cross-checks against published data (e.g. Brouwer/Nivasch 3-row Chomp, Sun 2004).

The author is responsible for every result. Papers from this project will disclose AI assistance according to the venue's policy (e.g. arXiv's). AI tools are not listed as authors.

## 3. Secrets

API keys are never committed. Put them in `.env`, which is git-ignored (see `.env.example`). CI runs a gitleaks secrets scan on every push.
