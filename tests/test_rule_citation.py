from judgment_formal_lint.api import parse_document
from judgment_formal_lint.rules import run_all_rules


def _leads(text):
    return run_all_rules(text, parse_document(text))


def test_cite01_zero_article():
    text = "依据《中华人民共和国民事诉讼法》第0条作出裁定。"
    hits = [l for l in _leads(text) if l.rule_id == "CITE-01"]
    assert hits


def test_cite01_valid_citation_not_flagged():
    text = "依据《中华人民共和国民法典》第五百七十七条作出判决。"
    assert not [l for l in _leads(text) if l.rule_id == "CITE-01"]
