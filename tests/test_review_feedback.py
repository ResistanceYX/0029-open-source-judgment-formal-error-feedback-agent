import json
import pytest

from judgment_formal_lint.api import lint_text
from judgment_formal_lint.review import apply_action
from judgment_formal_lint.feedback import build_feedback_draft


@pytest.fixture()
def report_file(tmp_path):
    report, _ = lint_text(str(tmp_path / "doc.txt"), "2023年2月30日签订。")
    p = tmp_path / "doc.txt.report.json"
    p.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
    return p


def test_review_accept_and_audit(tmp_path, report_file):
    apply_action(str(report_file), "accept", "DATE-01", 1, "核对正式文本后确认为笔误", "tester")
    report = json.loads(report_file.read_text(encoding="utf-8"))
    assert report["leads"][0]["review_status"] == "接受"
    audit = (tmp_path / "audit_log.jsonl").read_text(encoding="utf-8").strip()
    entry = json.loads(audit.splitlines()[-1])
    assert entry["action"] == "accept" and entry["reviewer"] == "tester"
    assert entry["reason"]


def test_review_reject_then_escalate(tmp_path, report_file):
    apply_action(str(report_file), "reject", "DATE-01", 1, "系农历日期", "tester")
    apply_action(str(report_file), "escalate", "DATE-01", 1, "需法律人士判断", "tester")
    report = json.loads(report_file.read_text(encoding="utf-8"))
    assert report["leads"][0]["review_status"] == "升级"


def test_review_unknown_action_raises(report_file):
    with pytest.raises(ValueError):
        apply_action(str(report_file), "submit", "DATE-01")


def test_review_unknown_rule_raises(report_file):
    with pytest.raises(ValueError):
        apply_action(str(report_file), "accept", "NOPE-99")


def test_feedback_draft_uses_only_accepted(tmp_path, report_file):
    report = json.loads(report_file.read_text(encoding="utf-8"))
    draft = build_feedback_draft(report)
    assert "没有经人工「接受」的线索" in draft

    apply_action(str(report_file), "accept", "DATE-01", 1, "已核对", "tester")
    report = json.loads(report_file.read_text(encoding="utf-8"))
    draft = build_feedback_draft(report)
    assert "未提交" in draft and "裁判文书网" in draft
    assert "错判" not in draft
    assert "2023年2月30日" in draft
