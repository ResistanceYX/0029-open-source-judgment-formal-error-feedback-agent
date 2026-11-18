# 复现指南

## 环境要求

- Python ≥ 3.10（开发验证环境：Linux Python 3.11/3.12、Windows 见 CI 矩阵）
- 核心工具零第三方运行时依赖；测试需要 pytest（`pip install -e ".[dev]"`）

## 安装

```bash
python -m pip install -e ".[dev]"
```

## 运行测试

```bash
python -m pytest tests -q
```

预期：39 项测试全部通过（规则正/反/边界例 + 端到端 + CLI 冒烟）。

## 跑合成样例

```bash
judgment-formal-lint lint examples/synthetic/sample_anomalies.txt -o /tmp/out
judgment-formal-lint lint examples/synthetic/sample_clean.txt -o /tmp/out
```

预期：`sample_anomalies.txt` 触发 8 类规则线索；`sample_clean.txt` 触发 0 条并显示
"无告警不等于文书没有错误"。

## 完整工作流演示

```bash
# 1. 检查 → JSON + Markdown 报告
judgment-formal-lint lint examples/synthetic/sample_anomalies.txt

# 2. 人工复核（接受 DATE-01 第 1 条，写入审计日志）
judgment-formal-lint review examples/synthetic/sample_anomalies.txt.report.json     accept --rule DATE-01 --reason "已核对正式文本，确认为笔误" --reviewer "你的名字"

# 3. 生成反馈草稿（只含已接受线索，不自动提交）
judgment-formal-lint feedback examples/synthetic/sample_anomalies.txt.report.json     -o feedback_draft.md
```

## 已知限制

- 只支持 UTF-8 纯文本（TXT/Markdown）；PDF/扫描件需先经合规的本地转换；
- 当事人识别依赖"角色：名称"式定义，其他称谓体系不覆盖；
- 金额核对只在段落句子级进行，跨段落合计不在 v1 范围；
- 大写金额解析只支持"元"为单位、不含"角/分"。
