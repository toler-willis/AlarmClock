#!/usr/bin/env python3
"""Convert Unity test runner stdout to JUnit XML.

Enriches each <testcase> name with any `@tests:ID` annotations found in a
comment directly above the matching test function in the source file, so
Ketryx picks up the tested-item-id linkage from the XML alone.

Usage:
    unity_to_junit.py <unity_log> <output_xml> <source_file> [<source_file> ...]
"""
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

UNITY_LINE = re.compile(r"^(?P<file>[^:]+):(?P<line>\d+):(?P<name>[^:]+):(?P<status>PASS|FAIL|IGNORE)(?::(?P<msg>.*))?$")
ANNOTATION = re.compile(r"@tests:([A-Za-z0-9_,\s\-]+)")


def collect_annotations(sources):
    """Map { test_function_name -> "@tests:ID1, @tests:ID2" } from source files."""
    out = {}
    for src in sources:
        text = Path(src).read_text()
        lines = text.splitlines()
        for idx, line in enumerate(lines):
            m = re.match(r"^\s*(?:static\s+)?void\s+(test_[A-Za-z0-9_]+)\s*\(", line)
            if not m:
                continue
            fn = m.group(1)
            for lookback in range(idx - 1, max(idx - 6, -1), -1):
                prev = lines[lookback]
                if not prev.strip():
                    continue
                tags = ANNOTATION.findall(prev)
                if tags:
                    ids = [t.strip() for group in tags for t in group.split(",")]
                    out[fn] = " ".join(f"@tests:{i}" for i in ids if i)
                break
    return out


def parse_unity_log(log_path):
    results = []
    for raw in Path(log_path).read_text().splitlines():
        m = UNITY_LINE.match(raw.strip())
        if not m:
            continue
        results.append(m.groupdict())
    return results


def build_xml(results, annotations, suite_name):
    failures = sum(1 for r in results if r["status"] == "FAIL")
    skipped = sum(1 for r in results if r["status"] == "IGNORE")
    suites = ET.Element("testsuites")
    suite = ET.SubElement(
        suites,
        "testsuite",
        name=suite_name,
        tests=str(len(results)),
        failures=str(failures),
        errors="0",
        skipped=str(skipped),
    )
    for r in results:
        name = r["name"]
        if name in annotations:
            name = f"{name} {annotations[name]}"
        tc = ET.SubElement(suite, "testcase", name=name, classname=suite_name)
        if r["status"] == "FAIL":
            fail = ET.SubElement(tc, "failure", message=(r["msg"] or "").strip())
            fail.text = (r["msg"] or "").strip()
        elif r["status"] == "IGNORE":
            ET.SubElement(tc, "skipped")
    return ET.ElementTree(suites)


def main(argv):
    if len(argv) < 4:
        print(__doc__, file=sys.stderr)
        return 2
    log_path, out_path, *sources = argv[1:]
    annotations = collect_annotations(sources)
    results = parse_unity_log(log_path)
    suite_name = Path(sources[0]).stem
    tree = build_xml(results, annotations, suite_name)
    ET.indent(tree, space="  ")
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    tree.write(out_path, encoding="utf-8", xml_declaration=True)
    print(f"Wrote {len(results)} test cases to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
