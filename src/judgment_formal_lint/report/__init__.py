"""报告层：JSON 报告 + Markdown 报告。字段与规则包版本绑定，可审计、可重跑。"""
from .json_report import build_json_report, REPORT_SCHEMA_VERSION
from .markdown_report import build_markdown_report

__all__ = ["build_json_report", "build_markdown_report", "REPORT_SCHEMA_VERSION"]
