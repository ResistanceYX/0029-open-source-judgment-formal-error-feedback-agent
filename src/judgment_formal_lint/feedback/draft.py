"""反馈草稿生成。

边界（对应 #0029 政策风险与执行人限制）：
- 仅使用复核状态为「接受」的线索；默认不自动提交、不批量留言、不使用他人登录态；
- 措辞为中性补正线索，不出现"错判/改判/违法"等定性词；
- 对事实认定、证据采信、裁判结论的异议提示走法定程序，不混入文书补正反馈。
"""
from __future__ import annotations

OFFICIAL_CHANNELS = (
    "1. 中国裁判文书网「意见建议」/针对单篇文书的留言入口；\n"
    "2. 向公布该文书的法院书面申请更正或补正（依据《最高人民法院关于人民法院在互联网公布裁判文书的规定》）；\n"
    "3. 涉及笔误的，可依法申请补正裁定；\n"
    "4. 对事实认定、证据采信或裁判结论有异议的，应通过上诉、再审等法定程序提出，不属于文书补正范围。"
)


def build_feedback_draft(report: dict) -> str:
    accepted = [lead for lead in report["leads"] if lead["review_status"] == "接受"]
    doc = report["document"]
    lines: list[str] = []
    lines.append("# 文书补正反馈草稿（未提交）")
    lines.append("")
    lines.append("> ⚠️ 本文件仅为草稿：请人工核对正式文本、确认措辞与事实后，由您本人选择渠道提交。"
                 "本工具不会、也不能代为提交。")
    lines.append("")
    lines.append(f"- 文书指纹：`{doc['sha256'][:16]}`")
    lines.append(f"- 规则包版本：`{report['rule_pack_version']}`")
    lines.append(f"- 已确认线索：{len(accepted)} 条")
    lines.append("")
    if not accepted:
        lines.append("当前没有经人工「接受」的线索，无法生成反馈草稿。")
        lines.append("")
        return "\n".join(lines)
    lines.append("## 建议核对事项")
    lines.append("")
    for i, lead in enumerate(accepted, 1):
        lines.append(f"{i}. （{lead['rule_id']}，第 {lead['para']} 段）{lead['explanation']}"
                     f"原文：{lead['excerpt']}")
    lines.append("")
    lines.append("## 提交前自检")
    lines.append("")
    lines.append("- 已核对法院正式文本（非转载/快照）；")
    lines.append("- 每项均有正式文本位置可回指；")
    lines.append("- 措辞为中性补正请求，不含对错定性；")
    lines.append("- 不含当事人隐私等不应公开的信息。")
    lines.append("")
    lines.append("## 既有官方渠道指引")
    lines.append("")
    lines.append(OFFICIAL_CHANNELS)
    lines.append("")
    return "\n".join(lines)
