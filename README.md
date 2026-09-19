# sreg project website

Website: https://jutrifonov.github.io/sreg-project/

Documentation for estimation and inference in stratified randomized experiments, with R, Stata, and Python implementations.

## Edit and publish

The editable pages and assets are in `source/`; the shared layout is in `overrides/`. The site is built with Zensical. GitHub Pages publishes the generated `docs/` directory on the `main` branch.

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/zensical build --strict
python3 check_site.py
touch docs/.nojekyll
```

Commit both the source changes and updated `docs/`, then push to `main`. GitHub Pages automatically publishes the updated files. For a local preview, run `.venv/bin/zensical serve`.

## Contents

- Introductory walkthrough for R, Stata, and Python
- Detailed R guide and reference
- Empirical application using the Peru encouragement experiment
- Supported experimental designs and methodological references
- Companion paper section, awaiting the manuscript

The package logo belongs to the sreg project. The homepage illustration was generated for this website. The empirical figure is based on results computed with R sreg 2.1.0.
