# Grant compliance checklist

Checklist for the AI for Math Fund seed grant (Renaissance Philanthropy, funded by XTX Markets): what each requirement asks, and where this repository satisfies it.

> **Source of the requirements:** the applicant's notes on the call, *not yet checked against the official call text*. Verify each row against the current RFP before submitting.
>
> **Funding status:** no grant has been awarded. `funding.yaml` has `funded: false`, and no funding acknowledgment is displayed anywhere.

## Requirements and evidence

| Requirement | Evidence in this repository | Status |
|---|---|---|
| **Open-source code** (OSI license) | [`LICENSE`](https://github.com/gargarnav/overthink-conjecture-engine/blob/main/LICENSE) (MIT); SPDX headers on every source file, enforced in CI (`scripts/check_spdx.py`); [`THIRD_PARTY_NOTICES.md`](https://github.com/gargarnav/overthink-conjecture-engine/blob/main/THIRD_PARTY_NOTICES.md), generated from package metadata (one dependency flagged and explained: a CC0 component in numpy); Lean MIT/Apache-2.0 compatibility noted in `lean/README.md` | Done |
| **Open datasets with documentation** | Dataset cards (description, motivation, schema with types, generation command and git commit, seeds, size, limitations, license, citation, SHA-256) in `datasets/<id>/README.md`; manifests; samples under 5 MB; `datasets/LICENSE` (CC BY 4.0); conjecture registry export `datasets/conjecture_registry/` (refuted conjectures kept); packaging `overthink package-dataset`; guide `datasets/PUBLISHING.md` | Done in repo |
| ↳ public hosting with DOI | Software: Zenodo DOI [10.5281/zenodo.23350597](https://doi.org/10.5281/zenodo.23350597), release v0.1.0 (code, cards, manifests, samples, registry export). Full data files: attached to the [GitHub release](https://github.com/gargarnav/overthink-conjecture-engine/releases/tag/v0.1.0); separate Zenodo dataset record pending. Hugging Face mirror optional. | Software done; dataset DOI **TODO (manual)** |
| **Open preprints** (arXiv) | None yet. Candidate first preprint: the W({a,a+1}) note ([write-up](results/W_pair_theorem.md)), after specialist review | **TODO** |
| **Acknowledgment on all outputs** | Text stored once in `funding.yaml`; inactive (`funded: false`). Locations listed below. | Ready, inactive (correct while unfunded) |
| **Budget rules**: indirect costs ≤ 10%, no visa costs | The budget is kept *out of this public repository* (`grant/` is git-ignored). Measured compute and API costs for the justification are in [costs](costs.md) (`overthink costs`). | **TODO (applicant, private)** |
| **Relevance** (AI for mathematics) | AI conjecture proposer with a checkable claim language; falsification at ≥10×; Lean 4 proofs; [methodology](methodology.md), `AI_USAGE.md` | Evidence in repo |
| **Catalytic potential** | Open datasets and conjecture registry as a benchmark; reusable pipeline (`overthink run`, Docker); `ROADMAP.md`; `CONTRIBUTING.md` | Evidence in repo |
| **Outputs** | Datasets (70M rows); 1,162 registry entries with status; 44 hand-written + 511 generated Lean theorems; pre-registered experiment reports. See [metrics](metrics.md), which also explains what the counts mean. | Evidence in repo |
| **Originality / novelty** | One possibly new theorem (P-positions of W({a,a+1}) for every a), pending specialist review; falsification-first method with pre-registration; honest negatives (blind rediscovery 0/4) | Evidence in repo; novelty to confirm |
| **Expertise** | Author's 4×n Chomp paper (arXiv:2604.25952, OEIS A395126) and its corrections found by this system; `CITATION.cff` with ORCID | Evidence in repo; other publications go in the private application |
| **Reproducibility** (supports Outputs) | `uv.lock`, `.python-version`, `lean/lean-toolchain`, `lean/lake-manifest.json`; `Dockerfile` (tested: Python and Rust tests pass in the container; the Lean variant is not tested locally); `make reproduce-demo` (regenerates the blind Chomp run and checks it exactly); CI on every push | Done |

## Where the acknowledgment goes once a grant is awarded

Switch `funded: true` in `funding.yaml`, then update:

1. `README.md`: the "Funding" section.
2. `CITATION.cff`: add the funder (e.g. under `references` or the abstract), and the DOI.
3. Dataset cards: rerun `overthink generate experiments/configs/datasets/*.yaml`; the cards include the acknowledgment automatically when funded.
4. Docs site footer: the `copyright:` line in `mkdocs.yml`.
5. Papers: uncomment `paper/acknowledgments.tex`.
6. `.zenodo.json`: add the grant to the description, and release notes.

## Separation from commercial work

Everything in this repository is open source and stays that way. Any future commercial work (for example smart-contract verification services) would live in a separate private repository, would not be funded by the grant, and this repository must never import from it. No commercial code is included here.

## Manual steps for the applicant

- [ ] **Verify the official call text** and update the requirement rows above.
- [x] **Zenodo software DOI:** integration on; release v0.1.0 archived as 10.5281/zenodo.23350598 (concept 10.5281/zenodo.23350597).
- [ ] **Zenodo dataset DOI:** upload the six `dist/datasets/*.zip` archives (also attached to the v0.1.0 GitHub release) as a Zenodo *Dataset* record, CC BY 4.0, "is supplement to" 10.5281/zenodo.23350597 (`datasets/PUBLISHING.md`).
- [ ] **Hugging Face** (optional): create an account and upload the packaged datasets (`datasets/PUBLISHING.md`).
- [x] **GitHub Pages:** source GitHub Actions, `PAGES_ENABLED = true`; docs site at https://gargarnav.github.io/overthink-conjecture-engine/.
- [ ] **Security reporting:** *Settings → Security → Private vulnerability reporting: enable*.
- [ ] **Contact email:** replace `TODO-CONTACT-EMAIL` in `CODE_OF_CONDUCT.md` and `SECURITY.md`.
- [x] **Project website:** `CITATION.cff` `url` points to the docs site. (The company domain is deliberately not used for this open-source project.)
- [ ] **ORCID:** already in `CITATION.cff` and `.zenodo.json` (0009-0009-2362-1903); check the ORCID profile lists the arXiv paper.
- [ ] **Novelty of the W({a,a+1}) theorem:** ask a specialist (e.g. an author of arXiv:2307.12458) and check Duchêne–Fraenkel–Nowakowski–Rigo (JCTA 2010).
- [ ] **Private application materials** (overview, milestones, team, budget, public benefit, catalytic plan) are kept outside this repository.
