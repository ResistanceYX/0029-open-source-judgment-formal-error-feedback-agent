from judgment_formal_lint.api import parse_document
from judgment_formal_lint.rules import run_all_rules


def _leads(text):
    return run_all_rules(text, parse_document(text))


def test_num01_wrong_total():
    text = "医疗费 3,000.00 元、误工费 2,000.00 元，以上共计 6,000.00 元。"
    leads = _leads(text)
    hits = [l for l in leads if l.rule_id == "NUM-01"]
    assert len(hits) == 1
    assert "5000" in hits[0].calculation and "6000" in hits[0].calculation


def test_num01_not_triggered_when_correct():
    text = "医疗费 3,000.00 元、误工费 2,000.00 元，以上共计 5,000.00 元。"
    assert not [l for l in _leads(text) if l.rule_id == "NUM-01"]


def test_num01_ignores_other_sentences():
    text = ("赔偿款 100,000.00 元。\n\n"
            "医疗费 3,000.00 元、误工费 2,000.00 元，以上共计 5,000.00 元。")
    assert not [l for l in _leads(text) if l.rule_id == "NUM-01"]


def test_num02_upper_lower_mismatch():
    text = "违约金为人民币壹万元整（9,000.00 元）。"
    leads = _leads(text)
    hits = [l for l in leads if l.rule_id == "NUM-02"]
    assert len(hits) == 1
    assert "10000" in hits[0].calculation


def test_num02_not_triggered_when_consistent():
    text = "违约金为人民币壹万元整（10,000.00 元）。"
    assert not [l for l in _leads(text) if l.rule_id == "NUM-02"]
