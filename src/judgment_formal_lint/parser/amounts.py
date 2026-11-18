"""金额解析：小写金额、大写金额，以及大写中文数字转换。"""
from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal

AMOUNT_RE = re.compile(r"(?:人民币)?\s*([0-9][0-9,]*(?:\.[0-9]{1,2})?)\s*元")
TOTAL_MARK_RE = re.compile(r"(?:合计|共计|总计|以上共计|上述共计)")
CN_UPPER_DIGITS = {"零": 0, "壹": 1, "贰": 2, "叁": 3, "肆": 4,
                   "伍": 5, "陆": 6, "柒": 7, "捌": 8, "玖": 9}
CN_UPPER_AMOUNT_RE = re.compile(
    r"人民币\s*([零壹贰叁肆伍陆柒捌玖拾佰仟万亿圆]+)\s*元\s*(整|正)?"
)


def upper_cn_to_int(s: str) -> int:
    """把大写中文金额整数部分转成 int。无法解析返回 -1。"""
    total, section, num = 0, 0, 0
    units = {"拾": 10, "佰": 100, "仟": 1000}
    big = {"万": 10000, "亿": 100000000}
    for ch in s:
        if ch in CN_UPPER_DIGITS:
            num = CN_UPPER_DIGITS[ch]
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
class AmountMention:
    value: Decimal
    surface: str
    para: int
    start: int
    end: int
    is_upper: bool = False


def find_amounts(paragraphs: list[tuple[int, str]]) -> list[AmountMention]:
    out: list[AmountMention] = []
    for para, ptext in paragraphs:
        for m in AMOUNT_RE.finditer(ptext):
            out.append(AmountMention(Decimal(m.group(1).replace(",", "")),
                                     m.group(0), para, m.start(), m.end()))
        for m in CN_UPPER_AMOUNT_RE.finditer(ptext):
            v = upper_cn_to_int(m.group(1))
            if v >= 0:
                out.append(AmountMention(Decimal(v), m.group(0), para,
                                       m.start(), m.end(), is_upper=True))
    out.sort(key=lambda x: (x.para, x.start))
    return out
