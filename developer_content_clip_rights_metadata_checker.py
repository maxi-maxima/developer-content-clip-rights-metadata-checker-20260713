#!/usr/bin/env python
"""Check publishing-rights metadata for short developer-content clips."""

import argparse
import csv
import json
import re
from pathlib import Path

REQUIRED = ("source_url", "license", "creator", "consent", "ai_generated_disclosure")
CLEAR_CONSENT = {"yes", "true", "granted", "public-domain", "public_domain", "approved"}
KNOWN_LICENSES = {
    "cc-by-4.0",
    "cc-by-sa-4.0",
    "cc0-1.0",
    "mit",
    "apache-2.0",
    "public-domain",
    "public_domain",
    "proprietary-with-permission",
}


def load_meta(path):
    p = Path(path)
    if p.suffix.lower() == ".json":
        return json.loads(p.read_text(encoding="utf-8"))
    if p.suffix.lower() == ".csv":
        with p.open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        if len(rows) != 1:
            raise ValueError(f"CSV metadata files must contain exactly one row: {path}")
        return rows[0]
    data = {}
    for line in p.read_text(encoding="utf-8").splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data


def discover_inputs(paths):
    files = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            files.extend(
                sorted(
                    child
                    for child in p.rglob("*")
                    if child.is_file() and child.suffix.lower() in {".json", ".csv", ".txt", ".md"}
                )
            )
        else:
            files.append(p)
    return files


def check(path):
    meta = load_meta(path)
    missing = [key for key in REQUIRED if not str(meta.get(key, "")).strip()]
    warnings = []

    source_url = str(meta.get("source_url", "")).strip()
    if source_url and not re.match(r"https?://", source_url):
        warnings.append("source_url is not http(s)")

    consent = str(meta.get("consent", "")).strip().lower()
    if consent and consent not in CLEAR_CONSENT:
        warnings.append("consent is not clearly granted")

    license_value = str(meta.get("license", "")).strip().lower()
    if license_value and license_value not in KNOWN_LICENSES:
        warnings.append("license is not in known allow-list")

    disclosure = str(meta.get("ai_generated_disclosure", "")).strip().lower()
    if disclosure in {"no", "none", "false", "n/a"}:
        warnings.append("ai_generated_disclosure should describe the disclosure shown to viewers")

    return {
        "file": str(path),
        "status": "FAIL" if missing or warnings else "PASS",
        "missing": missing,
        "warnings": warnings,
    }


def summarize(results):
    passed = sum(1 for result in results if result["status"] == "PASS")
    failed = len(results) - passed
    warning_count = sum(len(result["warnings"]) for result in results)
    missing_count = sum(len(result["missing"]) for result in results)
    return {
        "checked": len(results),
        "passed": passed,
        "failed": failed,
        "warnings": warning_count,
        "missing_required_fields": missing_count,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check clip metadata before publishing developer content snippets.")
    parser.add_argument("metadata", nargs="+", help="Metadata files or directories to scan")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    parser.add_argument("--summary", action="store_true", help="Include aggregate pass/fail counts")
    args = parser.parse_args(argv)

    inputs = discover_inputs(args.metadata)
    results = [check(path) for path in inputs]
    summary = summarize(results)

    if args.json:
        payload = {"summary": summary, "results": results} if args.summary else results
        print(json.dumps(payload, indent=2))
        return 1 if summary["failed"] else 0

    print("# Developer content clip rights metadata report\n")
    if args.summary:
        print(
            f"Checked: {summary['checked']}  Passed: {summary['passed']}  "
            f"Failed: {summary['failed']}  Warnings: {summary['warnings']}\n"
        )
    print("| status | file | missing | warnings |\n|---|---|---|---|")
    for result in results:
        print(
            f"| {result['status']} | {result['file']} | "
            f"{', '.join(result['missing']) or '-'} | {', '.join(result['warnings']) or '-'} |"
        )
    return 1 if summary["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
