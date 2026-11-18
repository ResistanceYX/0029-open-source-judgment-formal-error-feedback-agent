"""线索数据结构：与报告 Schema 一一对应。"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict


@dataclass
class Lead:
    rule_id: str
    severity: str            # 高 / 中 / 低
    confidence: str            # 高 / 中 / 低
    para: int                # 段落号
    offset: int              # 全文字符偏移（近似）
    excerpt: str             # 最小必要原文
    explanation: str         # 触发原因（确定性描述）
    calculation: str = ""    # 计算过程（如适用）
    alternatives: list = field(default_factory=list)  # 备选解释
    review_status: str = "待核"  # 待核/接受/驳回/编辑/升级

    def to_dict(self) -> dict:
        return asdict(self)


def excerpt_of(text: str, start: int, end: int, width: int = 28) -> str:
    a = max(0, start - width)
    b = min(len(text), end + width)
    snippet = text[a:b].replace("\n", " ")
    return ("…" if a > 0 else "") + snippet + ("…" if b < len(text) else "")
