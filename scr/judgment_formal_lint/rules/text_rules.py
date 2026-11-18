"""文本异常规则 TEXT-01/02：字符重复与标点异常。低争议、保守触发。"""
from __future__ import annotations

import re

from .base import Lead

REPEAT_CHAR_RE = re.compile(r"([一-龥])\1+")
FUNCTION_CHARS = set("的地得了是在和就都也很有其与此及或")
LEGAL_REDUP = {
    "人人", "天天", "刚刚", "处处", "年年", "月月", "日日", "多多", "常常",
    "谢谢", "看看", "想想", "说说", "走走", "往往", "渐渐", "纷纷", "频频",
    "恰恰", "仅仅", "区区", "赫赫", "鼎鼎", "寥寥", "莘莘", "堂堂", "彬彬",
    "翼翼", "洋洋", "滚滚", "统统", "个个", "件件", "条条", "款款", "项项",
    "步步", "层层", "面面", "点点", "滴滴", "丝丝", "微微", "略略", "稍稍",
    "好好", "大大", "小小", "早早", "慢慢", "快快速", "久久", "牢牢", "稳稳",
}
REPEAT_PUNCT_RE = re.compile(r"([，。！？；：、])\1+")


def run_text_rules(text: str, parsed: dict) -> list[Lead]:
    leads: list[Lead] = []
    for para, ptext in parsed["paragraphs"]:
        # TEXT-01 连续重复汉字
        for m in REPEAT_CHAR_RE.finditer(ptext):
            word = m.group(0)
            ch = m.group(1)
            if word in LEGAL_REDUP:
                continue
            if ch in FUNCTION_CHARS:
                conf, sev = "中", "中"
            else:
                conf, sev = "低", "低"
            leads.append(Lead(
                rule_id="TEXT-01", severity=sev, confidence=conf,
                para=para, offset=m.start(), excerpt=word,
                explanation=f"出现连续重复字符「{word}」",
                alternatives=["修辞叠词", "排版或 OCR 错误", "确有笔误，需核对正式文本"],
            ))
        # TEXT-02 连续重复标点
        for m in REPEAT_PUNCT_RE.finditer(ptext):
            leads.append(Lead(
                rule_id="TEXT-02", severity="低", confidence="中",
                para=para, offset=m.start(), excerpt=m.group(0),
                explanation=f"出现连续重复标点「{m.group(0)}」",
                alternatives=["强调性排版", "复制粘贴残留", "标点误用，需核对正式文本"],
            ))
    return leads
