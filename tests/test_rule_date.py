from judgment_formal_lint.api import parse_document
from judgment_formal_lint.rules import run_all_rules


def _leads(text):
    return run_all_rules(text, parse_document(text))


def test_date01_invalid_calendar_date():
    leads = _leads("2023年2月30日签订。")
    assert any(l.rule_id == "DATE-01" and l.confidence == "高" for l in leads)


def test_date01_not_triggered_on_leap_day():
    leads = _leads("2024年2月29日签订。")
    assert not [l for l in leads if l.rule_id == "DATE-01"]


def test_date02_multiple_spellings():
    text = "合同于2023-03-05签订。落款日期为二〇二三年三月五日。"
    leads = _leads(text)
    assert any(l.rule_id == "DATE-02" for l in leads)


def test_date03_reversed_range():
    text = "自2023年5月1日至2023年4月1日，被告占用房屋。"
    leads = _leads(text)
    assert any(l.rule_id == "DATE-03" for l in leads)


def test_date03_not_triggered_on_ordered_range():
    text = "自2023年4月1日至2023年5月1日，被告占用房屋。"
    leads = _leads(text)
    assert not [l for l in leads if l.rule_id == "DATE-03"]
