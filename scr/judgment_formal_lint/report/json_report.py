"""JSON 报告：含文书指纹、规则包版本、全部线索与统计。"""
from __future__ import annotations

from datetime import datetime, timezone

REPORT_SCHEMA_VERSION = "1.0.0"

DISCLAIMER = (
    "本报告只包含形式异常待核线索，不是错判认定、不是裁判结论评价；"
    "无告警不等于文书没有错误；任何使用须以法院正式文本为准并经人工核对。"
)


def build_json_report(document: dict, leads: list, tool_version: str,
                      rule_pack_version: str) -> dict:
    by_rule: dict[str, int] = {}
    by_severity: dict[str, int] = {}
    for lead in leads:
        by_rule[lead.rule_id] = by_rule.get(lead.rule_id, 0) + 1
        by_severity[lead.severity] = by_severity.get(lead.severity, 0) + 1
    return {
        "report_schema_version": REPORT_SCHEMA_VERSION,
        "tool_version": tool_version,
        "rule_pack_version": rule_pack_version,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "document": document,
        "disclaimer": DISCLAIMER,
        "stats": {
            "lead_count": len(leads),
            "by_rule": by_rule,
            "by_severity": by_severity,
        },
        "leads": [lead.to_dict() for lead in leads],
    }
