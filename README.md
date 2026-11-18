# 0029 · 开源裁判文书形式异常检测反馈工具

> idea-tree #0029 节点的开源实现仓库：`0029-open-source-judgment-formal-error-feedback-agent`
>
> **本工具只输出"待核线索"，不做裁判结论认定。** 形式异常可检 ≠ 实质错判；
> 无告警 ≠ 文书没有错误；任何使用须以法院正式文本为准并经人工核对。

## 这是什么

对用户合法取得或明确授权的裁判文书，检查**形式异常线索**：日期合法性、
金额合计与大小写、当事人称谓一致性、低争议文本异常、法条引注格式——
输出含原文位置、规则来源、计算过程、备选解释和置信度的复核报告，
并能把人工确认的线索生成为反馈草稿（含官方渠道指引）。

本工具不抓取任何平台、不自动提交任何反馈、不判断判决对错。

## 快速开始

```bash
python -m pip install -e ".[dev]"
python -m pytest tests -q                      # 39 项测试
judgment-formal-lint lint examples/synthetic/sample_anomalies.txt
```

三个子命令：

| 命令 | 作用 |
|---|---|
| `lint <file> [-o dir]` | 登记→解析→规则→输出 JSON+Markdown 报告 |
| `review <report> accept\|reject\|edit\|escalate --rule X [--occurrence N] [--reason R]` | 人工复核，全程审计 |
| `feedback <report> [-o draft.md]` | 已接受线索 → 反馈草稿（不自动提交） |

## 规则包 v1.0.0（8 条确定性规则）

| 规则 | 检查内容 |
|---|---|
| DATE-01/02/03 | 公历非法日期 / 同一日期多写法 / 时间区间倒置 |
| NUM-01/02 | 分项与合计不符 / 大小写金额不一致 |
| PARTY-01 | 当事人名称与全文用字相似但不同（简称、匿名写法不报） |
| TEXT-01/02 | 连续重复汉字 / 连续重复标点 |
| CITE-01 | 法条条号格式异常（不判断效力版本） |

详见 [docs/RULES.md](docs/RULES.md)。

## 能力边界

- 只处理用户主动提供的本地文件（TXT/Markdown）；
- 只输出待核线索：每条含位置、原文、规则、计算过程、备选解释、置信度；
- 反馈只生成草稿，由人工核对后自行选择官方渠道提交；
- 不认定错判、不替代上诉/再审/补正裁定等法定程序。

详见 [docs/BOUNDARIES.md](docs/BOUNDARIES.md)、[docs/DATA_GOVERNANCE.md](docs/DATA_GOVERNANCE.md)。

## 与上游项目的关系

本项目全部代码为重新实现，未复制 judicial-doc-anomaly-mcp、legal-hallucination-mcp、
judicial-doc-quality-mcp 的任何代码（其中第二个仓库没有 LICENSE 文件，代码不可复制）。
思想来源与核查记录见 [UPSTREAM.md](UPSTREAM.md)。

## 测试与验收

- 39 项自动化测试：规则正/反/边界例、报告 Schema、复核审计、反馈草稿边界、端到端、CLI 冒烟；
- 合成样例 2 篇：`sample_clean.txt`（0 线索）、`sample_anomalies.txt`（植入 8 类异常）；
- 测试只证明规则按预期触发，**不构成真实文书检出率证明**；
- 复现步骤见 [docs/REPRODUCE.md](docs/REPRODUCE.md)。

## 许可证

MIT（见 [LICENSE](LICENSE)）。文案与规则说明采用中性措辞，不构成法律意见。
