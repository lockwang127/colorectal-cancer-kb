#!/usr/bin/env python3
"""Validate colorectal cancer knowledge-base source files."""

import json
import re
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
SCHEMAS_DIR = BASE_DIR / "schemas"

# 颜色代码（Mac终端）
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
MAX_MESSAGES_PER_FILE = 20
CURRENT_REQUIRED_FIELDS = ["head", "relation", "tail", "source", "evidence", "domain"]
LEGACY_REQUIRED_FIELDS = ["subject", "predicate", "object", "source", "evidence_level", "confidence"]
STANDARD_EVIDENCE = {"I级", "II级", "III级", "专家共识", "Guideline", "Literature"}

def print_success(msg):
    print(f"{GREEN}✅ {msg}{RESET}")

def print_warning(msg):
    print(f"{YELLOW}⚠️  {msg}{RESET}")

def print_error(msg):
    print(f"{RED}❌ {msg}{RESET}")


def print_messages(messages, printer):
    for message in messages[:MAX_MESSAGES_PER_FILE]:
        printer(message)
    omitted = len(messages) - MAX_MESSAGES_PER_FILE
    if omitted > 0:
        print_warning(f"还有 {omitted} 条同类信息未展开显示")


def has_current_relation_fields(item):
    return any(field in item for field in ("head", "relation", "tail", "evidence"))


def has_legacy_relation_fields(item):
    return any(field in item for field in ("subject", "predicate", "object", "evidence_level"))


def validate_relation_item(item, index):
    errors = []
    warnings = []

    if not isinstance(item, dict):
        errors.append(f"第{index}条数据应为对象")
        return errors, warnings

    if has_current_relation_fields(item):
        required_fields = CURRENT_REQUIRED_FIELDS
        evidence_field = "evidence"
    elif has_legacy_relation_fields(item):
        required_fields = LEGACY_REQUIRED_FIELDS
        evidence_field = "evidence_level"
    else:
        errors.append(f"第{index}条：无法识别关系字段，应使用 head/relation/tail")
        return errors, warnings

    for field in required_fields:
        if field not in item:
            errors.append(f"第{index}条数据缺少必填字段：{field}")
        elif item[field] in ("", None):
            errors.append(f"第{index}条数据字段为空：{field}")

    evidence = item.get(evidence_field)
    if evidence and isinstance(evidence, str) and evidence not in STANDARD_EVIDENCE:
        if not any(token in evidence for token in ("级", "指南", "共识", "研究", "文献", "trial", "Trial", "RCT")):
            warnings.append(f"第{index}条：{evidence_field} 值较不规范：{evidence}")

    if "confidence" in item:
        confidence = item["confidence"]
        if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            warnings.append(f"第{index}条：confidence 应为0.0-1.0之间的数值")

    if "conditions" in item and not isinstance(item["conditions"], dict):
        warnings.append(f"第{index}条：conditions 建议使用对象格式")

    return errors, warnings


def validate_json_file(file_path):
    """校验JSON文件格式"""
    errors = []
    warnings = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"JSON格式错误：{e}")
        return errors, warnings
    
    # 检查是否为数组
    if not isinstance(data, list):
        errors.append("数据应为JSON数组格式")
        return errors, warnings
    
    seen = set()
    legacy_count = 0
    for i, item in enumerate(data, start=1):
        if isinstance(item, dict) and has_legacy_relation_fields(item):
            legacy_count += 1
        item_errors, item_warnings = validate_relation_item(item, i)
        errors.extend(item_errors)
        warnings.extend(item_warnings)

        if isinstance(item, dict):
            key = (
                item.get("head") or item.get("subject"),
                item.get("relation") or item.get("predicate"),
                item.get("tail") or item.get("object"),
                item.get("source"),
            )
            if key in seen:
                warnings.append(f"第{i}条：可能重复的三元组")
            seen.add(key)

    if legacy_count:
        warnings.append(f"文件包含 {legacy_count} 条早期 subject/predicate/object 字段，后续可逐步迁移到 head/relation/tail")
    
    return errors, warnings


def validate_markdown_file(file_path):
    """校验Markdown文件格式"""
    errors = []
    warnings = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        errors.append(f"无法读取文件：{e}")
        return errors, warnings
    
    # 检查frontmatter
    if not content.startswith('---'):
        warnings.append("缺少YAML frontmatter（--- 分隔符）")
    else:
        # 提取frontmatter
        match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if match:
            frontmatter = match.group(1)
            # 检查必填字段
            required = ["title", "year", "source", "type", "tags"]
            for field in required:
                if f"{field}:" not in frontmatter:
                    warnings.append(f"Frontmatter缺少字段：{field}")
    
    # 版权检查（简单关键词检测）
    copyright_keywords = ["版权所有", "Copyright", "All rights reserved", "请勿转载"]
    for keyword in copyright_keywords:
        if keyword in content:
            warnings.append(f"检测到可能的版权声明词汇：{keyword}（请确认非原文复制）")
    
    return errors, warnings


def scan_directory():
    """扫描整个data目录，校验所有文件"""
    print("\n" + "="*60)
    print("结直肠癌知识库 - 数据校验报告")
    print("="*60 + "\n")
    
    total_files = 0
    passed_files = 0
    total_errors = 0
    total_warnings = 0
    
    # 1. 校验JSON文件
    print("📊 校验JSON数据文件...\n")
    
    json_files = list((DATA_DIR / "knowledge-graph").glob("*.json"))
    for json_file in json_files:
        total_files += 1
        print(f"检查：{json_file.relative_to(BASE_DIR)}")
        
        errors, warnings = validate_json_file(json_file)
        total_errors += len(errors)
        total_warnings += len(warnings)
        
        if errors:
            print_messages(errors, print_error)
        if warnings:
            print_messages(warnings, print_warning)
        if not errors and not warnings:
            print_success("格式正确")
            passed_files += 1
        print()
    
    # 2. 校验Markdown文件
    print("\n📝 校验Markdown文件...\n")
    
    md_files = list((DATA_DIR / "guidelines").rglob("*.md"))
    for md_file in md_files:
        total_files += 1
        print(f"检查：{md_file.relative_to(BASE_DIR)}")
        
        errors, warnings = validate_markdown_file(md_file)
        total_errors += len(errors)
        total_warnings += len(warnings)
        
        if errors:
            print_messages(errors, print_error)
        if warnings:
            print_messages(warnings, print_warning)
        if not errors and not warnings:
            print_success("格式正确")
            passed_files += 1
        print()
    
    # 3. 打印汇总
    print("="*60)
    print(f"校验完成：")
    print(f"  - 总文件数：{total_files}")
    print(f"  - 通过：{passed_files}")
    print(f"  - 错误：{total_errors}")
    print(f"  - 警告：{total_warnings}")
    print("="*60)
    
    if total_errors > 0:
        print_error("存在错误，请修正后再提交！")
        return False
    elif total_warnings > 0:
        print_warning("存在警告，请检查确认。")
        return True
    else:
        print_success("所有文件格式正确！")
        return True


if __name__ == "__main__":
    success = scan_directory()
    exit(0 if success else 1)
