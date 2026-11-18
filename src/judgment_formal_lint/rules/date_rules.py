"""日期规则 DATE-01/02/03：只核对公历合法性与可定位的形式矛盾。"""
from __future__ import annotations

from .base import Lead
from ..parser.dates import DateMention


def _date_range_text(dm: DateMention) -> str:
    return f"{dm.year}年{dm.month}月{dm.day}日"


def run_date_rules(text: str, parsed: dict) -> list[Lead]:
    leads: list[Lead] = []
    dates: list[DateMention] = parsed["dates"]

    # DATE-01 非法公历日期（如 2023年2月30日）
    for dm in dates:
        if not dm.valid:
            leads.append(Lead(
                rule_id="DATE-01", severity="高", confidence="高",
                para=dm.para, offset=0, excerpt=dm.surface,
                explanation=f"{dm.surface} 不是公历合法日期（{_date_range_text(dm)} 无法落在真实日历上）",
                calculation=f"datetime.date({dm.year}, {dm.month}, {dm.day}) -> ValueError",
                alternatives=["原文可能是农历/其他历法", "排版或 OCR 识别错误", "确有笔误，需核对正式文本"],
            ))

    # DATE-02 同一日期多种写法（归一化后相同、表面写法不同）
    groups: dict[str, list[DateMention]] = {}
    for dm in dates:
        groups.setdefault(dm.normalized, []).append(dm)
    for norm, members in groups.items():
        surfaces = {m.surface for m in members}
        if len(surfaces) >= 2:
            first = members[0]
            leads.append(Lead(
                rule_id="DATE-02", severity="低", confidence="低",
                para=first.para, offset=0, excerpt=first.surface,
                explanation=f"日期 {norm} 在文中以多种写法出现：{'、'.join(sorted(surfaces))}",
                alternatives=["不同位置格式习惯不同（落款与正文）", "不同写作人/排版阶段造成", "其中一处可能有笔误"],
            ))

    # DATE-03 同一行内“自X至Y”式时间区间倒置
    import re
    line_pair = re.compile(
        r"自(?P<a>[^。\n]{0,20}?(?:\d{4}\s*[年\-/\.]\s*\d{1,2}\s*[月\-/\.]\s*\d{1,2}\s*日?|"
        r"[零〇一二两三四五六七八九]{4}年[^。，；\n]{0,10}日))"
        r"(?:起)?\s*(?:至|到|—|–|-|~)\s*"
        r"(?P<b>\d{4}\s*[年\-/\.]\s*\d{1,2}\s*[月\-/\.]\s*\d{1,2}\s*日?|"
        r"[零〇一二两三四五六七八九]{4}年[^。，；\n]{0,10}日)")
    for para, ptext in parsed["paragraphs"]:
        for m in line_pair.finditer(ptext):
            from ..parser.dates import ARABIC_DATE_RE, CN_DATE_RE, cn_to_int
            a_text, b_text = m.group("a"), m.group("b")
            da = ARABIC_DATE_RE.search(a_text) or CN_DATE_RE.search(a_text)
            db = ARABIC_DATE_RE.search(b_text) or CN_DATE_RE.search(b_text)
            if not da or not db:
                continue
            if hasattr(da, "group") and "y" in da.re.groupindex:
                ta = (int(da.group("y")), int(da.group("m")), int(da.group("d")))
                tb = (int(db.group("y")), int(db.group("m")), int(db.group("d")))
            else:
                ta = (cn_to_int(da.group("y")), cn_to_int(da.group("m")), cn_to_int(da.group("d")))
                tb = (cn_to_int(db.group("y")), cn_to_int(db.group("m")), cn_to_int(db.group("d")))
            if -1 in ta or -1 in tb:
                continue
            if ta > tb:
                off = 0
                leads.append(Lead(
                    rule_id="DATE-03", severity="中", confidence="中",
                    para=para, offset=off, excerpt=m.group(0),
                    explanation=f"时间区间起点 {ta[0]}-{ta[1]:02d}-{ta[2]:02d} 晚于终点 {tb[0]}-{tb[1]:02d}-{tb[2]:02d}，区间倒置",
                    calculation=f"({ta[0]}, {ta[1]}, {ta[2]}) > ({tb[0]}, {tb[1]}, {tb[2]})",
                    alternatives=["起止字样排版错位", "把两个不同区间写在了一句", "确有笔误，需核对正式文本"],
                ))
    return leads
