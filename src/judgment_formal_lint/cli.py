"""命令行入口：lint / review / feedback 三个子命令。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .api import lint_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="judgment-formal-lint",
        description="裁判文书形式异常线索检查工具（只输出待核线索，不做裁判结论）")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_lint = sub.add_parser("lint", help="检查一篇文书，输出 JSON+Markdown 报告")
    p_lint.add_argument("file", help="文书文本路径（TXT/Markdown）")
    p_lint.add_argument("-o", "--out", default=None, help="报告输出目录（默认与文书同目录）")

    p_rev = sub.add_parser("review", help="对报告中的线索执行人工复核动作")
    p_rev.add_argument("report", help="报告 JSON 路径")
    p_rev.add_argument("action", choices=["accept", "reject", "edit", "escalate"])
    p_rev.add_argument("--rule", required=True, help="规则 ID，如 DATE-01")
    p_rev.add_argument("--occurrence", type=int, default=1, help="同规则第几条（默认 1）")
    p_rev.add_argument("--reason", default="", help="复核理由（建议填写）")
    p_rev.add_argument("--reviewer", default="local-user")

    p_fb = sub.add_parser("feedback", help="把已接受的线索生成为反馈草稿")
    p_fb.add_argument("report", help="报告 JSON 路径")
    p_fb.add_argument("-o", "--out", default=None, help="草稿输出路径（默认打印到 stdout）")

    args = parser.parse_args(argv)

    if args.cmd == "lint":
        report = lint_file(args.file, args.out)
        print(f"文书指纹 {report['document']['sha256'][:16]} ｜ "
              f"触发 {report['stats']['lead_count']} 条线索")
        for rule, count in sorted(report["stats"]["by_rule"].items()):
            print(f"  {rule}: {count}")
        print(f"JSON 报告: {report['outputs']['json']}")
        print(f"Markdown 报告: {report['outputs']['markdown']}")
        print("提醒：以上均为待核线索，须人工核对正式文本。")
        return 0

    if args.cmd == "review":
        from .review import apply_action
        apply_action(args.report, args.action, args.rule, args.occurrence,
                     args.reason, args.reviewer)
        print(f"已对 {args.rule} 第 {args.occurrence} 条执行 {args.action}，审计已记录。")
        return 0

    if args.cmd == "feedback":
        from .feedback import build_feedback_draft
        report = json.loads(Path(args.report).read_text(encoding="utf-8"))
        draft = build_feedback_draft(report)
        if args.out:
            Path(args.out).write_text(draft, encoding="utf-8")
            print(f"草稿已写入 {args.out}（未提交）")
        else:
            print(draft)
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
