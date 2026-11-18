"""把文书文本切成段落，并给出稳定的 段落号/字符偏移 定位。"""
from __future__ import annotations

import re


def split_paragraphs(text: str) -> list[tuple[int, str]]:
    """返回 [(段落号, 段落文本)]，按空行分段；无空行则按行分段。"""
    chunks = re.split(r"\n\s*\n", text.strip())
    paras: list[tuple[int, str]] = []
    if len(chunks) <= 1:
        for line in text.splitlines():
            if line.strip():
                paras.append((len(paras) + 1, line.strip()))
        return paras
    for c in chunks:
        c = c.strip()
        if c:
            paras.append((len(paras) + 1, c))
    return paras


def char_offset(text: str, para_index: int, match_start_in_para: int) -> int:
    """把段内偏移换算为全文偏移（近似：按段落顺序累加长度+分隔符）。"""
    base = 0
    paras = re.split(r"\n\s*\n", text.strip())
    for i in range(min(para_index, len(paras))):
        base += len(paras[i]) + 2
    return base + match_start_in_para
