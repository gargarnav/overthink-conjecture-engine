# Security policy

Please **do not open public issues** for security problems (for example, a leaked credential, or a way to make the claim parser execute code).

Report privately through GitHub's private vulnerability reporting: *Security → Report a vulnerability* on this repository. Alternatively, email the maintainer at gargarnav2007@gmail.com.

Scope notes:
- LLM claims are parsed with a whitelist and compiled to Polars expressions; nothing is `eval`-ed (`src/overthink/conjecture/claims.py`). Bypasses of that whitelist are in scope.
- Secrets must never be committed; CI runs gitleaks on every push.
