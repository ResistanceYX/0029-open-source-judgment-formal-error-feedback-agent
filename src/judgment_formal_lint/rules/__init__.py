"""规则包：只输出待核线索，不做裁判结论、不判断法条效力、不做实质对错认定。"""
from __future__ import annotations

from .base import Lead
from .date_rules import run_date_rules
from .num_rules import run_num_rules
from .party_rules import run_party_rules
from .text_rules import run_text_rules
from .citation_rules import run_citation_rules

RULE_PACK_VERSION = "1.0.0"

__all__ = ["Lead", "RULE_PACK_VERSION", "run_all_rules"]


def run_all_rules(text: str, parsed: dict) -> list[Lead]:
    leads: list[Lead] = []
    leads += run_date_rules(text, parsed)
    leads += run_num_rules(text, parsed)
    leads += run_party_rules(text, parsed)
    leads += run_text_rules(text, parsed)
    leads += run_citation_rules(text, parsed)
    leads.sort(key=lambda x: (x.para, x.offset))
    return leads
