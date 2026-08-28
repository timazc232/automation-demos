# actions-ci

校验一份 JSON / YAML 周报 fixture。字段不对就退出码 1，方便放进 GitHub Actions，PR 里直接红。

Validates a weekly-report JSON/YAML file. Non-zero exit if invalid.

## 自动化什么

团队把本周事项写进 `reports/YYYY-Www.json`（或 yaml）。CI 检查：

- `week` 形如 `2026-W34`
- `author` 非空
- `items` 非空列表，每项有 `title`、`status`（`done` / `wip` / `blocked` / `planned`）

不发邮件、不调外部 API。就是一个小校验器。

## 本地跑

```bash
# 在仓库根目录
pip install pyyaml pytest
python actions-ci/validate_report.py actions-ci/fixtures/valid.json    # 退出 0
python actions-ci/validate_report.py actions-ci/fixtures/invalid.json  # 退出 1
pytest actions-ci/tests
```

## 拷到客户仓库

1. 复制 `validate_report.py` 到客户仓库（路径自定）。
2. 复制 [`examples/weekly-report.yml`](examples/weekly-report.yml) 为 `.github/workflows/weekly-report.yml`。
3. 改 workflow 里的 `python validate_report.py ...` 指向客户的周报文件。
4. 不需要 secret。报告内容是仓库里的普通文件。

本目录的测试和 fixture 是给这个 demo 用的，客户仓库一般只留校验脚本 + workflow。
