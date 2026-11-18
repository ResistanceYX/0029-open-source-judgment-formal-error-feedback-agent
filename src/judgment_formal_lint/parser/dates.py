"""日期解析：阿拉伯数字日期、中文小写日期，以及中文数字转换。"""
from __future__ import annotations

import re
from dataclasses import dataclass

CN_DIGITS = {"〇": 0, "零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4,
             "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
_CN_NUM = {"〇": 0, "零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5,
           "六": 6, "七": 7, "八": 8, "九": 9}

ARABIC_DATE_RE = re.compile(
    r"(?P<y>\d{4})\s*(?:年|[-/.])\s*(?P<m>\d{1,2})\s*(?:月|[-/.])\s*(?P<d>\d{1,2})\s*日?"
)
CN_DATE_RE = re.compile(
    r"(?P<y>[零〇一二两三四五六七八九]{4})\s*年\s*(?P<m>[正一二两三四五六七八九十]{1,3})\s*月\s*(?P<d>[正一二两三四五六七八九十]{1,3})\s*日"
)


def cn_to_int(s: str) -> int:
    """把中文小写数字（支持十/百/千/万/亿）转成整数。无法解析时返回 -1。

    纯数字字符（无单位）的串按逐位念法处理，如"二〇二三"=2023。
    """
    if s.isdigit():
        return int(s)
    if s and all(ch in _CN_NUM for ch in s):
        value = 0
        for ch in s:
            value = value * 10 + _CN_NUM[ch]
        return value
    total, section, num = 0, 0, 0
    units = {"十": 10, "百": 100, "千": 1000}
    big = {"万": 10000, "亿": 100000000}
    for ch in s:
        if ch in _CN_NUM:
            num = _CN_NUM[ch]
        elif ch == "正" and s.strip("正") == "":
            return 1
        elif ch in units:
            section += (num if num else 1) * units[ch]
            num = 0
        elif ch in big:
            section = (section + num) * big[ch]
            total += section
            section, num = 0, 0
        else:
            return -1
    return total + section + num


@dataclass
class DateMention:
    year: int
    month: int
    day: int
    surface: str          # 原文写法
    normalized: str       # yyyy-mm-dd
    para: int
    start: int            # 段内偏移
    end: int
    valid: bool           # 是否公历合法日期


def _validate(y: int, m: int, d: int) -> bool:
    import datetime as _dt
    try:
        _dt.date(y, m, d)
        return True
    except ValueError:
        return False


def find_dates(paragraphs: list[tuple[int, str]]) -> list[DateMention]:
    out: list[DateMention] = []
    for para, ptext in paragraphs:
        for m in ARABIC_DATE_RE.finditer(ptext):
            y, mo, d = int(m.group("y")), int(m.group("m")), int(m.group("d"))
            out.append(DateMention(y, mo, d, m.group(0), f"{y:04d}-{mo:02d}-{d:02d}",
                                   para, m.start(), m.end(), _validate(y, mo, d)))
        for m in CN_DATE_RE.finditer(ptext):
            y = cn_to_int(m.group("y"))
            mo = cn_to_int(m.group("m"))
            d = cn_to_int(m.group("d"))
            if y < 0 or mo < 0 or d < 0:
                continue
            out.append(DateMention(y, mo, d, m.group(0), f"{y:04d}-{mo:02d}-{d:02d}",
                                   para, m.start(), m.end(), _validate(y, mo, d)))
    out.sort(key=lambda x: (x.para, x.start))
    return out
