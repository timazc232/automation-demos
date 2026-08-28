# workspace-script

用 CSV 模拟 Google Sheet：列是 date, owner, task, status, due。
按负责人汇总 open / wip / blocked，打出 markdown 或纯文本周报。

Python 侧不调用 Google API。测试全程离线。真正发信要接到 Apps Script。

Models Sheets to weekly digest email. Tests use a fixture CSV, not live Gmail.

## 本地跑（离线）

    pip install pytest
    python workspace-script/weekly_digest.py workspace-script/fixtures/tasks.csv
    python workspace-script/weekly_digest.py workspace-script/fixtures/tasks.csv --format text
    pytest workspace-script/tests

## 接到客户 Workspace（clasp）

客户必须自己授权。域名内批量代发通常需要 Workspace 管理员同意 OAuth。
本仓库不代客户登录、不存 refresh token。

安装 clasp 后：clasp login，再 clasp create --type sheets，把 appsscript.json 与 Code.gs.example（改名 Code.gs）放进目录后 clasp push。

## OAuth scopes（见 appsscript.json）

- spreadsheets.readonly — 读任务表
- gmail.send — 把摘要发到授权用户邮箱

不要向脚本要整盘 Drive、不要要 Gmail 只读全箱。客户审 scopes 时按最小权限批。

Code.gs.example 是对照 Python 逻辑的注释样例，CI 不会执行它。
