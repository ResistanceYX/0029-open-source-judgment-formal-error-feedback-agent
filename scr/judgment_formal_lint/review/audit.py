"""人工复核动作与审计日志。审计记录追加到报告同目录 audit_log.jsonl。"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ACTION_TO_STATUS = {
    "accept": "接受",
    "reject": "驳回",
    "edit": "编辑",
    "escalate": "升级",
}


def apply_action(report_path: str, action: str, rule_id: str,
                 occurrence: int = 1, reason: str = "",
                 reviewer: str = "local-user") -> dict:
    """对报告中第 occurrence 条 rule_id 线索执行人工动作，返回更新后的报告。"""
    if action not in ACTION_TO_STATUS:
        raise ValueError(f"未知动作 {action}，可选：{sorted(ACTION_TO_STATUS)}")
    p = Path(report_path)
    report = json.loads(p.read_text(encoding="utf-8"))
    matches = [i for i, lead in enumerate(report["leads"]) if lead["rule_id"] == rule_id]
    if not matches:
        raise ValueError(f"报告中没有规则 {rule_id} 的线索")
    if occurrence > len(matches):
        raise ValueError(f"规则 {rule_id} 只有 {len(matches)} 条线索")
    idx = matches[occurrence - 1]
    old_status = report["leads"][idx]["review_status"]
    report["leads"][idx]["review_status"] = ACTION_TO_STATUS[action]
    p.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    audit_entry = {
        "time": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "rule_id": rule_id,
        "lead_index": idx,
        "old_status": old_status,
        "new_status": ACTION_TO_STATUS[action],
        "reason": reason,
        "reviewer": reviewer,
        "document_id": report["document"]["document_id"],
        "rule_pack_version": report["rule_pack_version"],
    }
    audit_path = p.parent / "audit_log.jsonl"
    with audit_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(audit_entry, ensure_ascii=False) + "\n")
    return report
