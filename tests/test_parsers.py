from judgment_formal_lint.parser.segment import split_paragraphs
from judgment_formal_lint.parser.dates import find_dates, cn_to_int
from judgment_formal_lint.parser.amounts import find_amounts, upper_cn_to_int
from judgment_formal_lint.parser.parties import find_party_defs
from judgment_formal_lint.parser.citations import find_citations


def test_segment_by_blank_line():
    paras = split_paragraphs("first para.\n\nsecond para.")
    assert [p for p, _ in paras] == [1, 2]


def test_cn_to_int():
    assert cn_to_int("2023") == 2023
    assert cn_to_int("十") == 10
    assert cn_to_int("二十") == 20
    assert cn_to_int("二百五十一") == 251


def test_dates_arabic_and_cn():
    paras = [(1, "2023年2月30日签订。二〇二三年三月五日落款。")]
    dates = find_dates(paras)
    assert len(dates) == 2
    assert dates[0].valid is False
    assert dates[1].valid is True
    assert dates[1].normalized == "2023-03-05"


def test_amounts():
    paras = [(1, "医疗费 3,000.00 元，违约金人民币壹万元整。")]
    amts = find_amounts(paras)
    assert len(amts) == 2
    assert amts[0].value == 3000
    assert amts[1].value == 10000 and amts[1].is_upper


def test_upper_cn_to_int():
    assert upper_cn_to_int("壹万") == 10000
    assert upper_cn_to_int("伍佰") == 500


def test_party_defs():
    paras = [(1, "原告：张三。被告：某某科技有限公司。")]
    defs = find_party_defs(paras)
    assert [(d.role, d.name) for d in defs] == [("原告", "张三"), ("被告", "某某科技有限公司")]


def test_citations():
    paras = [(1, "依据《中华人民共和国民法典》第五百七十七条、《民事诉讼法》第0条。")]
    cites = find_citations(paras)
    assert len(cites) == 2
    assert cites[0].article == 577
    assert cites[1].article == 0
