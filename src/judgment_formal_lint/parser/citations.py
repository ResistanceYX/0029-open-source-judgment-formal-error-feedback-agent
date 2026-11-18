"""法条引注解析：只做结构化提取与格式检查，不判断效力版本。"""
from __future__ import annotations

import re
from dataclasses import dataclass

from .dates import cn_to_int

CITE_RE = re.compile(
    r"《(?P<law>[^《》\n]{2,40})》\s*第(?P<article>[0-9零〇一二两三四五六七八九十百千]+)条"
    r"(?:\s*第(?P<section>[0-9零〇一二两三四五六七八九十]+)款)?"
    r"(?:\s*第(?P<item>[0-9零〇一二两三四五六七八九十]+)项)?"
)


@dataclass
class Citation:
    law: str
    article_raw: str
    article: int
    section_raw: str | None
    section: int | None
    item_raw: str | None
    item: int | None
    para: int
    start: int
    end: int
    surface: str


def find_citations(paragraphs: list[tuple[int, str]]) -> list[Citation]:
    out: list[Citation] = []
    for para, ptext in paragraphs:
        for m in CITE_RE.finditer(ptext):
            art = cn_to_int(m.group("article"))
            if art < 0:
                continue
            sec_raw = m.group("section")
            item_raw = m.group("item")
            sec = cn_to_int(sec_raw) if sec_raw else None
            item = cn_to_int(item_raw) if item_raw else None
            out.append(Citation(
                law=m.group("law").strip(),
                article_raw=m.group("article"), article=art,
                section_raw=sec_raw, section=sec,
                item_raw=item_raw, item=item,
                para=para, start=m.start(), end=m.end(), surface=m.group(0)))
    return out
