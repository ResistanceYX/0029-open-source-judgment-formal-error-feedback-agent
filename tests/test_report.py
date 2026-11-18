import json
from judgment_formal_lint.api import lint_text
from judgment_formal_lint.report.json_report import REPORT_SCHEMA_VERSION
from judgment_formal_lint.rules import RULE_PACK_VERSION


def test_report_schema_fields():
    report, _ = lint_text("demo.txt", "2023年2月30日。")
    assert report["report_schema_version"] == REPORT_SCHEMA_VERSION
    assert report["rule_pack_version"] == RULE_PACK_VERSION
    assert report["stats"]["lead_count"] >= 1
    lead = report["leads"][0]
    for key in ("rule_id", "severity", "confidence", "para", "offset",
                "excerpt", "explanation", "alternatives", "review_status"):
        assert key in lead
    assert "无告警不等于文书没有错误" in report["disclaimer"]


def test_report_serializable():
    report, _ = lint_text("demo.txt", "content")
    json.dumps(report, ensure_ascii=False)


def test_markdown_contains_disclaimer_and_location():
    _, md = lint_text("demo.txt", "2023年2月30日。")
    assert "待核线索" in md and "正式文本" in md and "第 1 段" in md
