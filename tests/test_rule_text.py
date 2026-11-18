from judgment_formal_lint.api import parse_document
from judgment_formal_lint.rules import run_all_rules


def _leads(text):
    return run_all_rules(text, parse_document(text))


def test_text01_function_char_repeat():
    leads = _leads("这个的的 情况需要核实。")
    hits = [l for l in leads if l.rule_id == "TEXT-01"]
    assert hits and hits[0].severity == "中"


def test_text01_legitimate_reduplication_not_flagged():
    leads = _leads("人人 均应遵守法律。")
    assert not [l for l in leads if l.rule_id == "TEXT-01"]


def test_text02_repeated_punctuation():
    leads = _leads("情况属实！！本院予以确认。")
    hits = [l for l in leads if l.rule_id == "TEXT-02"]
    assert hits and hits[0].excerpt == "！！"
