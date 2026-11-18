"""合法输入登记：记录来源、取得方式、授权、下载时间、文件指纹、正式文本核验状态与允许用途。

对应 #0029 YAML 可拆零件第 1 项。本工具只处理用户主动提供并声明有权检查的材料；
不抓取、不镜像任何平台，不绕过任何访问控制。
"""
from __future__ import annotations

import hashlib
from datetime import datetime, timezone


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def register_input(path: str, text: str, authorization: str = "用户提供并声明有权检查该材料") -> dict:
    digest = sha256_text(text)
    return {
        "document_id": digest[:16],
        "sha256": digest,
        "source_path": str(path),
        "source_type": "user_provided_file",
        "authorization": authorization,
        "obtained_at": datetime.now(timezone.utc).isoformat(),
        "allowed_use": "形式异常线索检查与人工复核（不含任何自动提交、镜像或再分发）",
        "formal_text_verified": False,
        "formal_text_note": "以法院正式文本为准；使用前须由人工核对",
    }
