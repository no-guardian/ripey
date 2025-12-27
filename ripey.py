#!/usr/bin/env python3
# improved version by no-guardian (c) 2025

import argparse
import requests
import pandas as pd
import re
from ipaddress import ip_address, summarize_address_range

RIPE_API = "https://rest.db.ripe.net/search"

def fetch_ripe_results(query: str):
    params = {
        "query-string": query,
        "source": "ripe",
        "flags": "no-filtering",
        "format": "json"
    }

    headers = {
        "Accept": "application/json"
    }

    r = requests.get(
        "https://rest.db.ripe.net/search",
        params=params,
        headers=headers,
        timeout=20
    )

    r.raise_for_status()
    data = r.json()

    objects = data.get("objects", {}).get("object", [])
    records = []

    for obj in objects:
        record = {"__type": obj.get("type")}

        for attr in obj.get("attributes", {}).get("attribute", []):
            key = attr.get("name")
            value = attr.get("value")

            record[key] = (
                record[key] + " | " + value
                if key in record else value
            )

        records.append(record)

    return records

# def fetch_ripe_results(query: str):
#     params = {
#         "query-string": query,
#         "source": "ripe",
#         "flags": "no-filtering",
#         "format": "json"
#     }
# 
#     r = requests.get(RIPE_API, params=params, timeout=20)
#     r.raise_for_status()
# 
#     data = r.json()
# 
#     objects = data.get("objects", {}).get("object", [])
#     records = []
# 
#     for obj in objects:
#         record = {}
#         record["__type"] = obj.get("type")
# 
#         for attr in obj.get("attributes", {}).get("attribute", []):
#             key = attr.get("name")
#             value = attr.get("value")
# 
#             if key in record:
#                 record[key] += " | " + value
#             else:
#                 record[key] = value
# 
#         records.append(record)
# 
#     return records


def save_csv(records, filename="ripe.csv"):
    df = pd.DataFrame(records)
    df = df.reindex(sorted(df.columns), axis=1)
    df.to_csv(filename, index=False)


def extract_emails(records):
    emails = set()
    for record in records:
        for value in record.values():
            if isinstance(value, str):
                emails.update(
                    re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", value)
                )
    return sorted(emails)


def extract_subnets(records):
    subnets = set()

    for record in records:
        inet = record.get("inetnum")
        if inet and "-" in inet:
            start, end = [ip_address(x.strip()) for x in inet.split("-")]
            for subnet in summarize_address_range(start, end):
                subnets.add(str(subnet))

    return sorted(subnets)


def main():
    parser = argparse.ArgumentParser(description="RIPE database query tool (REST API)")
    parser.add_argument("query", help="Search query (domain, ASN, org, IP, etc)")
    parser.add_argument("-csv", action="store_true", help="Save results to CSV")
    parser.add_argument("-o", "--output", help="Output CSV file")
    parser.add_argument("-email", action="store_true", help="Extract email addresses")
    parser.add_argument("-subnet", action="store_true", help="Summarize IP ranges to subnets")

    args = parser.parse_args()

    records = fetch_ripe_results(args.query)

    if args.email:
        for email in extract_emails(records):
            print(email)

    elif args.subnet:
        for subnet in extract_subnets(records):
            print(subnet)

    elif args.csv:
        save_csv(records, args.output or "ripe.csv")

    else:
        for record in records:
            for k, v in record.items():
                print(f"{k}: {v}")
            print("-" * 40)


if __name__ == "__main__":
    main()
