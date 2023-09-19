# Thesis-o-meter

A wordcount tracker for our PhD dissertations.

## Setup

This assumes that you have your dissertation on GitHub and can use actions.

Set up a workflow that calculates your dissertation's word count on push to the main branch.
It should then clone this repo, add a line to your personal csv file and push the change back.

An example github workflow:

```yaml
name: Wordcount

on:
  push:
    branches:
      - main

jobs:
  wordcount:
    concurrency: wordcount
    runs-on: ubuntu-22.04
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Install Nix
        uses: DeterminateSystems/nix-installer-action@v4

      - name: Run the Magic Nix Cache
        uses: DeterminateSystems/magic-nix-cache-action@v1

      - name: Checkout thesis-o-meter
        uses: actions/checkout@v3
        with:
          repository: jeffa5/thesis-o-meter
          ref: main
          path: thesis-o-meter
          ssh-key: ${{ secrets.DEPLOY_KEY }}

      - name: Get and submit the wordcount
        run: |
          wordcount=$(nix run .#wordcount)
          datetime=$(date --rfc-3339=seconds | tr ' ' 'T')
          echo "$datetime,$wordcount"
          cd thesis-o-meter
          echo "$datetime,$wordcount" >> data/<user>.csv
          git add data/<user>.csv
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git commit -m "Update <user> wordcount"
          git push
```

This assumes a deploy key is setup to give read and write access to the thesis-o-meter repo and the private key is set as a secret for the actions run in `DEPLOY_KEY`.

## CSV format

Each person should have a CSV file at `data/<crsid|gh_username>.csv`.
The format is:

```csv
datetime,wordcount
2023-09-19T09:19:20,200
2023-09-20T20:37:22,424
```

The `datetime` field is rfc3339 formatted.
