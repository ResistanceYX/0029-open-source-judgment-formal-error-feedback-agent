"""Markdown 报告：人工复核友好格式，每条线索含位置、原文、规则、备选解释。"""
from __future__ import annotations

from .json_report import DISCLAIMER


def build_markdown_report(report: dict) -> str:
    doc = report["document"]
    stats = report["stats"]
    lines: list[str] = []
    lines.append("# 裁判文书形式异常待核线索报告")
    lines.append("")
    lines.append(f"- 文书指纹：`{doc['sha256'][:16]}`（SHA-256 前 16 位）")
    lines.append(f"- 规则包版本：`{report['rule_pack_version']}` ｜ 工具版本：`{report['tool_version']}`")
    lines.append(f"- 报告 Schema：`{report['report_schema_version']}` ｜ 生成时间：`{report['generated_at']}`")
    lines.append(f"- 线索总数：**{stats['lead_count']}**")
    lines.append("")
    lines.append(f"> ⚠️ {DISCLAIMER}")
    lines.append("")
    if stats["lead_count"] == 0:
        lines.append("## 结果")
        lines.append("")
        lines.append("未触发任何规则。**注意：无告警不等于文书没有错误**——规则覆盖有限，"
                     "实质性问题（事实认定、证据采信、法律适用）不在本工具范围内，")
        lines.append("请以法院正式文本为准。")
        lines.append("")
        return "\n".join(lines)
    lines.append("## 线索明细")
    lines.append("")
    for i, lead in enumerate(report["leads"], 1):
        lines.append(f"### {i}. [{lead['rule_id']}] {lead['explanation']}")
        lines.append("")
        lines.append(f"- 严重度/置信度：{lead['severity']} / {lead['confidence']}")
        lines.append(f"- 位置：第 {lead['para']} 段，全文字符偏移约 {lead['offset']}")
        lines.append(f"- 原文摘录：{lead['excerpt']}")
        if lead["calculation"]:
            lines.append(f"- 计算/比对过程：`{lead['calculation']}`")
        if lead["alternatives"]:
            lines.append(f"- 备选解释：{'；'.join(lead['alternatives'])}")
        lines.append(f"- 复核状态：{lead['review_status']}")
        lines.append("")
    lines.append("## 统计")
    lines.append("")
    lines.append("| 规则 | 触发次数 |")
    lines.append("|---|---|")
    for rule, count in sorted(stats["by_rule"].items()):
        lines.append(f"| {rule} | {count} |")
    lines.append("")
    return "\n".join(lines)
