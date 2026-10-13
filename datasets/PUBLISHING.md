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

## 2. Zenodo (DOI)

Recommended route: the GitHub integration, which archives every GitHub release with the metadata in `.zenodo.json`.

1. Sign in at https://zenodo.org with GitHub; under *Account → GitHub*, switch on `gargarnav/overthink-conjecture-engine`.
2. Create a GitHub release (e.g. `v0.1.0`) and attach the `dist/datasets/*.zip` archives as release assets. Zenodo archives the release, including the assets, and mints a DOI.
3. Put the DOI badge in `README.md` and the DOI in `CITATION.cff` (`identifiers:`).

Alternative: a separate Zenodo *dataset* upload of the archives (upload type "Dataset", license CC BY 4.0), linked to the software DOI with "is supplement to".

## 3. Hugging Face mirror (optional)

1. Create the dataset repository `gargarnav/overthink-<id>` (or one repository with one folder per dataset).
2. Upload `data.parquet`, `README.md` (dataset card) and `LICENSE` from the package directory, e.g. `huggingface-cli upload gargarnav/overthink-chomp4 dist/datasets/chomp4_n1000-v0.1.0 . --repo-type dataset`.
3. Add the Zenodo DOI to the card so the DOI copy stays canonical.

## Checklist per release

- [ ] `overthink verify` passes for every dataset
- [ ] cards regenerated from the current code (`overthink generate`)
- [ ] archives contain SHA256SUMS; spot-check one with `shasum -a 256 -c SHA256SUMS`
- [ ] GitHub release created with archives attached; Zenodo DOI minted
- [ ] DOI added to README, CITATION.cff and the dataset cards
