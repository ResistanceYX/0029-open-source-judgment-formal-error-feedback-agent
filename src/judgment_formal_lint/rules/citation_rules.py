"""法条引注规则 CITE-01：结构化提取 + 格式异常线索。明确不判断效力版本与适用正确性。"""
from __future__ import annotations

from .base import Lead


def run_citation_rules(text: str, parsed: dict) -> list[Lead]:
    leads: list[Lead] = []
    for c in parsed["citations"]:
        # CITE-01 条号格式异常（0 或明显超出合理范围）
        if c.article <= 0 or c.article > 2000:
            leads.append(Lead(
                rule_id="CITE-01", severity="中", confidence="中",
                para=c.para, offset=c.start, excerpt=c.surface,
                explanation=f"引注条号「{c.article_raw}」解析为 {c.article}，超出常见条号范围",
                calculation=f"cn_to_int('{c.article_raw}') = {c.article}",
                alternatives=["引注指向法律汇编条目而非条文", "排版或 OCR 错误", "确有笔误，需核对正式文本"],
            ))
        if c.section is not None and c.section > 20:
            leads.append(Lead(
                rule_id="CITE-01", severity="低", confidence="低",
                para=c.para, offset=c.start, excerpt=c.surface,
                explanation=f"引注款号「{c.section_raw}」解析为 {c.section}，偏大",
                alternatives=["款号排版错误", "确有笔误，需核对正式文本"],
            ))
    return leads
