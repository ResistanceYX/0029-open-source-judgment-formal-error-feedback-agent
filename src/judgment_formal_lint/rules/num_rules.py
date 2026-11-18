"""金额规则 NUM-01/02：分项合计核对、大小写金额核对。只展示计算过程，不裁决对错。"""
from __future__ import annotations

from collections import defaultdict
from decimal import Decimal

from .base import Lead


def run_num_rules(text: str, parsed: dict) -> list[Lead]:
    leads: list[Lead] = []
    amounts = parsed["amounts"]
    by_para: dict[int, list] = defaultdict(list)
    for a in amounts:
        by_para[a.para].append(a)

    import re
    from ..parser.amounts import TOTAL_MARK_RE

    # NUM-01 分项金额与合计核对（段落内）
    for para, plist in by_para.items():
        lowers = [a for a in plist if not a.is_upper]
        ptext = next((t for p, t in parsed["paragraphs"] if p == para), "")
        total_match = None
        for m in TOTAL_MARK_RE.finditer(ptext):
            tail = ptext[m.end():m.end() + 40]
            am = re.search(r"([0-9][0-9,]*(?:\.[0-9]{1,2})?)\s*元", tail)
            if am:
                total_match = (Decimal(am.group(1).replace(",", "")), m.start(), am.group(0))
                break
        if not total_match:
            continue
        total_value, t_off, t_surface = total_match
        # 只取"合计"所在句子（以 。；！？\n 为界）内、合计词之前的金额作为分项
        sent_start = max(ptext.rfind(x, 0, t_off) for x in "。；！？\n") + 1
        items = [a for a in lowers if sent_start <= a.start < t_off]
        items = [a for a in items if a.value != total_value]
        if len(items) < 2:
            continue
        item_sum = sum((a.value for a in items), Decimal("0"))
        if item_sum != total_value:
            calc = " + ".join(str(a.value) for a in items) + f" = {item_sum} ≠ 合计 {total_value}"
            leads.append(Lead(
                rule_id="NUM-01", severity="高", confidence="高",
                para=para, offset=t_off, excerpt=t_surface,
                explanation=f"段落内分项金额求和为 {item_sum} 元，与合计金额 {total_value} 元不符",
                calculation=calc,
                alternatives=["合计含未逐项列明项目", "计算口径差异（含税/不含税、利息截算）", "确有误算或漏算，需核对正式文本"],
            ))

    # NUM-02 大写金额与小写金额不一致
    for para, plist in by_para.items():
        uppers = [a for a in plist if a.is_upper]
        lowers = [a for a in plist if not a.is_upper]
        if not uppers or not lowers:
            continue
        for u in uppers:
            if any(l.value == u.value for l in lowers):
                continue  # 同段存在一致的小写金额，视为对应
            mismatch = [l for l in lowers if l.value != u.value]
            if mismatch:
                l = min(mismatch, key=lambda x: abs(x.value - u.value))
                leads.append(Lead(
                    rule_id="NUM-02", severity="中", confidence="中",
                    para=para, offset=u.start, excerpt=u.surface,
                    explanation=f"大写金额 {u.surface}（= {u.value} 元）与同段小写金额 {l.surface}（= {l.value} 元）不一致",
                    calculation=f"{u.value} != {l.value}",
                    alternatives=["大小写分别指向不同笔款项", "大写为约数或保底表述", "确有误写，需核对正式文本"],
                ))
    return leads
