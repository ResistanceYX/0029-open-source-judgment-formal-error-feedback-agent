import json
import subprocess
import sys
from pathlib import Path

from judgment_formal_lint.api import lint_file

ROOT = Path(__file__).resolve().parents[1]

DOC = """某市人民法院民事判决书

原告：张大山。被告：某某科技有限公司。

本院查明，2023年2月30日，双方签订施工合同。自2023年5月1日至2023年4月1日，被告占用施工现场。

经审理查明，工程款 100,000.00 元、质保金 10,000.00 元，以上共计 120,000.00 元。违约金约定为人民币伍万元整（40,000.00 元）。

张二山 在庭审中的陈述与查明事实不符。该的的 陈述缺乏证据支持！！

依照《中华人民共和国民事诉讼法》第0条、《中华人民共和国民法典》第八百零七条，判决如下。

二〇二三年六月一日 书记员 陈某"""


def test_end_to_end_detects_all_categories(tmp_path):
    p = tmp_path / "doc.txt"
    p.write_text(DOC, encoding="utf-8")
    report = lint_file(str(p), str(tmp_path))
    rules = {lead["rule_id"] for lead in report["leads"]}
    assert {"DATE-01", "DATE-03", "NUM-01", "NUM-02",
            "PARTY-01", "TEXT-01", "TEXT-02", "CITE-01"} <= rules
    assert Path(report["outputs"]["json"]).exists()
    assert Path(report["outputs"]["markdown"]).exists()


def test_clean_document_zero_leads(tmp_path):
    p = tmp_path / "clean.txt"
    p.write_text("原告：王五。\n\n2023年3月5日签订合同。货款 1,000.00 元。",
                 encoding="utf-8")
    report = lint_file(str(p), str(tmp_path))
    assert report["stats"]["lead_count"] == 0
    md = Path(report["outputs"]["markdown"]).read_text(encoding="utf-8")
    assert "无告警不等于文书没有错误" in md


def test_cli_smoke(tmp_path):
    p = tmp_path / "doc.txt"
    p.write_text(DOC, encoding="utf-8")
    import os
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    r = subprocess.run([sys.executable, "-m", "judgment_formal_lint.cli", "lint",
                        str(p), "-o", str(tmp_path)],
                       capture_output=True, text=True, env=env, timeout=60)
    assert r.returncode == 0, r.stderr
    assert "触发" in r.stdout
