# Ripey (RIPE REST API version)
original created by tedixx

rewritten by no-guardian 12-2025

A lightweight RIPE database query tool using the official RIPE REST API.

BE AWARE: the fulltextsearch is only allowed via the website; see https://docs.db.ripe.net/How-to-Query-the-RIPE-Database/Web-Query-Form#uri-format-fulltextsearch-select

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
```bash
python ripey.py example
python ripey.py example -email
python ripey.py example -subnet
python ripey.py example -csv -o output.csv
```
