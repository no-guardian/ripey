# Ripey (RIPE REST API version)

A lightweight RIPE database query tool using the official RIPE REST API.

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
