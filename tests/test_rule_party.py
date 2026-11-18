from judgment_formal_lint.api import parse_document
from judgment_formal_lint.rules import run_all_rules


def _leads(text):
    return run_all_rules(text, parse_document(text))


def test_party01_one_char_diff():
    text = "原告：张大山。\n\n张二山 到庭参加诉讼。"
    hits = [l for l in _leads(text) if l.rule_id == "PARTY-01"]
    assert len(hits) == 1 and "张二山" in hits[0].excerpt


def test_party01_anonymized_name_not_flagged():
    text = "原告：张三。\n\n张某 到庭参加诉讼。"
    assert not [l for l in _leads(text) if l.rule_id == "PARTY-01"]


def test_party01_abbreviation_not_flagged():
    text = "原告：华宇科技有限公司。\n\n华宇公司 在本案中为实际施工人。"
    assert not [l for l in _leads(text) if l.rule_id == "PARTY-01"]


def test_party01_company_typo():
    text = "被告：华宇科技有限公司。\n\n华宇科技有限公同 收到传票后未答辩。"
    hits = [l for l in _leads(text) if l.rule_id == "PARTY-01"]
    assert len(hits) == 1 and "公同" in hits[0].excerpt
