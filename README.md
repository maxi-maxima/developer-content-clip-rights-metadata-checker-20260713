# Developer Content Clip Rights Metadata Checker

## Pain point
DevRel teams cut demos, podcasts, and tutorials into short clips, but clip folders often lack source URL, license, speaker consent, and AI-generated disclosure metadata.

## Why now
AI media tools and content repurposing are booming; provenance and rights checks make small teams safer before publishing clips.

## Installation
Requires Python 3.9+ and no third-party dependencies.

```bash
git clone https://github.com/maxi-maxima/developer-content-clip-rights-metadata-checker-20260713.git
cd developer-content-clip-rights-metadata-checker-20260713
python developer_content_clip_rights_metadata_checker.py --help
```

## Run
```bash
$ python developer_content_clip_rights_metadata_checker.py examples/clip-good.json --summary
Checked: 1  Passed: 1  Failed: 0  Warnings: 0
| PASS | examples/clip-good.json | - | - |
```

Scan a whole folder of JSON, CSV, TXT, or Markdown metadata files:

```bash
python developer_content_clip_rights_metadata_checker.py ./clips --json --summary
```

The checker validates required fields, URL scheme, clear consent wording, known license values, and whether the AI disclosure is descriptive enough for viewer-facing provenance.

## Self-check
```bash
python -m unittest discover -s tests -v
python developer_content_clip_rights_metadata_checker.py examples --json --summary
```

## Example input/output
See `examples/`. The command above prints a Markdown or JSON report suitable for CI logs and pull request comments.

## Roadmap
- Add GitHub Actions workflow templates.
- Add SARIF or JSON schema output.
- Add more real-world fixture formats from agent, MCP, and DevRel tools.

## License
MIT
