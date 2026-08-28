[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

# automation-demos

接 GitHub Actions 周报校验、Google Workspace（Sheets → 邮件摘要）这类小自动化。电鸭 / V2EX / Upwork 可询。

GitHub Actions + Google Workspace automation samples. Not a SaaS — copy the bits you need.

## 两个 demo

| 目录 | 做什么 |
| --- | --- |
| [actions-ci/](actions-ci/) | 校验 JSON/YAML 周报 fixture；校验失败退出码非 0，方便挂进 GitHub Actions |
| [workspace-script/](workspace-script/) | 用 CSV 模拟 Sheet，按负责人汇总未完成任务，生成 markdown / 纯文本周报。测试不调 Google API |

## 本地跑测试

需要 Python 3.11+。不访问网络。

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

或分开跑：

```bash
pip install pytest pyyaml
pytest actions-ci/tests
pytest workspace-script/tests
```

## 这是 demo，不是产品

没有账号、没有后台、没有计费。仓库里没有 secret、没有真实 Gmail。CI 只跑 pytest。客户侧要接 Gmail / Sheets，自己走 OAuth，见 `workspace-script/README.md`。
