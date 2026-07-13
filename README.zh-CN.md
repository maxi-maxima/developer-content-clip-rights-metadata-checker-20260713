# Developer Content Clip Rights Metadata Checker

## 解决的痛点
DevRel teams cut demos, podcasts, and tutorials into short clips, but clip folders often lack source URL, license, speaker consent, and AI-generated disclosure metadata.

## 为什么现在值得做
AI media tools and content repurposing are booming; provenance and rights checks make small teams safer before publishing clips.

## 安装
需要 Python 3.9+，无第三方依赖。

```bash
git clone https://github.com/maxi-maxima/developer-content-clip-rights-metadata-checker-20260713.git
cd developer-content-clip-rights-metadata-checker-20260713
python developer_content_clip_rights_metadata_checker.py --help
```

## 运行
```bash
$ python developer_content_clip_rights_metadata_checker.py examples/clip-good.json
| PASS | examples/clip-good.json | - | - |
```

## 自检
```bash
python -m unittest discover -s tests
```

## 示例输入/输出
请查看 `examples/`。工具会输出适合 CI 日志和 Pull Request 评论的 Markdown 或 JSON 报告。

## 路线图
- 增加 GitHub Actions 模板。
- 增加 SARIF 或 JSON Schema 输出。
- 增加更多来自 Agent、MCP、DevRel 工具的真实格式样例。

## License
MIT
