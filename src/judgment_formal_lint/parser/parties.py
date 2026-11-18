"""当事人识别：只提取"角色: 名称"定义，不做人名真伪判断。"""
from __future__ import annotations

import re
from dataclasses import dataclass

ROLE_RE = re.compile(
    r"(原告|被告|上诉人|被上诉人|申请人|被申请人|原审原告|原审被告|第三人|申请执行人|被执行人)\s*[:：]\s*([^\n，。；;]{2,30})"
)
TOKEN_RE = re.compile(r"[一-龥A-Za-z0-9（）()]{2,20}")


@dataclass
class PartyDef:
    role: str
    name: str
    para: int
    start: int
    end: int


def find_party_defs(paragraphs: list[tuple[int, str]]) -> list[PartyDef]:
    out: list[PartyDef] = []
    for para, ptext in paragraphs:
        for m in ROLE_RE.finditer(ptext):
            out.append(PartyDef(m.group(1), m.group(2).strip(), para, m.start(), m.end()))
    return out


def all_tokens(text: str) -> list[tuple[str, int, int]]:
    """全文连续中/英/数字串（括号视为名称一部分）。"""
    return [(m.group(0), m.start(), m.end()) for m in TOKEN_RE.finditer(text)]
