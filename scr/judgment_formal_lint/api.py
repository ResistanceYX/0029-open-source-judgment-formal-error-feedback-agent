"""顶层 API：一次调用完成 登记→解析→规则→报告。"""
from __future__ import annotations

from pathlib import Path

from . import __version__
from .input_registry import register_input
from .parser.segment import split_paragraphs
from .parser.dates import find_dates
from .parser.amounts import find_amounts
from .parser.citations import find_citations
from .rules import run_all_rules, RULE_PACK_VERSION
from .report import build_json_report, build_markdown_report


def parse_document(text: str) -> dict:
    paragraphs = split_paragraphs(text)
    return {
        "paragraphs": paragraphs,
        "dates": find_dates(paragraphs),
        "amounts": find_amounts(paragraphs),
        "citations": find_citations(paragraphs),
    }


def lint_text(path: str, text: str) -> tuple[dict, str]:
    """返回 (json_report, markdown_report)。"""
    document = register_input(path, text)
    parsed = parse_document(text)
    leads = run_all_rules(text, parsed)
    report = build_json_report(document, leads, __version__, RULE_PACK_VERSION)
    return report, build_markdown_report(report)


def lint_file(path: str, out_dir: str | None = None) -> dict:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    report, md = lint_text(str(p), text)
    out = Path(out_dir) if out_dir else p.parent
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / (p.name + ".report.json")
    md_path = out / (p.name + ".report.md")
    json_path.write_text(__import__("json").dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(md, encoding="utf-8")
    report["outputs"] = {"json": str(json_path), "markdown": str(md_path)}
    return report
