# Publishing datasets

Full data files are never committed to git. A release is packaged locally, checked against the committed manifest, and published to **Zenodo** (permanent DOI, the citable copy) and optionally mirrored on **Hugging Face Datasets** (discoverability).

## 1. Package

```bash
uv run overthink generate experiments/configs/datasets/*.yaml          # rebuild data_out/
uv run overthink verify chomp4_n1000 chomp4_a3000_c60 wythoff_n1000 \
    subtraction_subsets9_n2000 wsub_subsets5_n1000                     # content hashes
uv run overthink package-dataset chomp4_n1000 chomp4_a3000_c60 wythoff_n1000 \
    subtraction_subsets9_n2000 wsub_subsets5_n1000 --version 0.1.0
```

Each archive `dist/datasets/<id>-v0.1.0.zip` contains `data.parquet`, the dataset card (`README.md`), `manifest.json`, `sample.parquet`, `LICENSE` (CC BY 4.0), `SHA256SUMS` and `RELEASE.json`. Packaging fails if the data does not match the committed manifest.

## 2. Zenodo (DOIs)

**Software DOI (automatic).** With the GitHub integration switched on (Zenodo → *Account → GitHub*), every GitHub release is archived with the metadata in `.zenodo.json`. Zenodo archives the release's **source snapshot only**: the code, dataset cards, manifests, samples and the conjecture registry export (all committed). Files attached to the GitHub release are *not* archived by the integration.

**Dataset DOI (manual upload).** The full Parquet files therefore need their own Zenodo record:

1. Zenodo → *New upload*. Upload the `dist/datasets/*.zip` archives.
2. Resource type **Dataset**; license **CC BY 4.0**; creator Arnav Garg (ORCID 0009-0009-2362-1903); title e.g. "Overthink Conjecture Engine datasets v0.1.0".
3. Related works: "Is supplement to" the software DOI (or the GitHub release URL).
4. Publish, then add the dataset DOI to `README.md`, `CITATION.cff` and the dataset cards.

The same archives are also attached to the GitHub release for direct download.

## 3. Hugging Face mirror (optional)

1. Create the dataset repository `gargarnav/overthink-<id>` (or one repository with one folder per dataset).
2. Upload `data.parquet`, `README.md` (dataset card) and `LICENSE` from the package directory, e.g. `huggingface-cli upload gargarnav/overthink-chomp4 dist/datasets/chomp4_n1000-v0.1.0 . --repo-type dataset`.
3. Add the Zenodo DOI to the card so the DOI copy stays canonical.

## Checklist per release

- [ ] `overthink verify` passes for every dataset
- [ ] cards regenerated from the current code (`overthink generate`)
- [ ] archives contain SHA256SUMS; spot-check one with `shasum -a 256 -c SHA256SUMS`
- [ ] GitHub release created with archives attached; software DOI minted
- [ ] dataset archives uploaded as a Zenodo dataset record; dataset DOI minted
- [ ] DOI added to README, CITATION.cff and the dataset cards
