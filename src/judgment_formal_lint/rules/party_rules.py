"""当事人规则 PARTY-01：定义名称与全文用字的相似性线索。简称与合理差异默认不报错。"""
from __future__ import annotations

import difflib

from .base import Lead
from ..parser.parties import find_party_defs, all_tokens


def _is_sub_or_super(short: str, long: str) -> bool:
    """是否一方为另一方的子串（视为简称/全称关系，不报）。"""
    return short in long or long in short


def run_party_rules(text: str, parsed: dict) -> list[Lead]:
    leads: list[Lead] = []
    defs = find_party_defs(parsed["paragraphs"])
    tokens = all_tokens(text)
    seen: set[tuple[str, str]] = set()
    for d in defs:
        for tok, t_start, t_end in tokens:
            if tok == d.name or len(tok) < 2:
                continue
            if tok[0] != d.name[0]:
                continue
            key = (d.name, tok)
            if key in seen:
                continue
            ratio = difflib.SequenceMatcher(None, d.name, tok).ratio()
            if _is_sub_or_super(tok, d.name):
                continue  # 简称/全称视为正常
            if "某" in tok:
                continue  # 张某/某某 属常见匿名写法
            if len(d.name) <= 3:
                hit = (len(tok) == len(d.name) and
                       sum(1 for a, b in zip(d.name, tok) if a != b) == 1)
            else:
                hit = ratio >= 0.75
            if not hit:
                continue
            seen.add(key)
            leads.append(Lead(
                rule_id="PARTY-01", severity="中", confidence="中",
                para=0, offset=t_start, excerpt=tok,
                explanation=f"当事人「{d.role}: {d.name}」与文中用字「{tok}」高度相似但不相同（相似度 {ratio:.2f}）",
                calculation=f"SequenceMatcher({d.name}, {tok}) = {ratio:.3f}",
                alternatives=["简称或习惯性简写", "同姓/同名不同主体", "排版或 OCR 错误", "确有笔误，需核对正式文本"],
            ))
    return leads
