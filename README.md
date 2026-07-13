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
$ python developer_content_clip_rights_metadata_checker.py examples/clip-good.json
| PASS | examples/clip-good.json | - | - |
```

## Self-check
```bash
python -m unittest discover -s tests
```

## Example input/output
See `examples/`. The command above prints a Markdown or JSON report suitable for CI logs and pull request comments.

## Roadmap
- Add GitHub Actions workflow templates.
- Add SARIF or JSON schema output.
- Add more real-world fixture formats from agent, MCP, and DevRel tools.

## License
MIT
