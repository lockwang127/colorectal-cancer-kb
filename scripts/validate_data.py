#!/usr/bin/env python3
"""
结直肠癌知识库 - 数据校验脚本
用于校验知识库中的数据格式是否符合规范
"""

import json
import os
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

def print_success(msg):
    print(f"{GREEN}✅ {msg}{RESET}")

def print_warning(msg):
    print(f"{YELLOW}⚠️  {msg}{RESET}")

def print_error(msg):
    print(f"{RED}❌ {msg}{RESET}")


def validate_json_file(file_path, schema_type="relation"):
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
    
    # 根据类型校验字段
    if schema_type == "relation":
        required_fields = ["subject", "predicate", "object", "evidence_level", "source", "contributor", "date_added", "confidence"]
        for i, item in enumerate(data):
            for field in required_fields:
                if field not in item:
                    errors.append(f"第{i+1}条数据缺少必填字段：{field}")
            
            # 检查 evidence_level
            if "evidence_level" in item:
                if item["evidence_level"] not in ["I级", "II级", "III级", "专家共识"]:
                    warnings.append(f"第{i+1}条：evidence_level 值不标准（应为 I级/II级/III级/专家共识）")
            
            # 检查 confidence
            if "confidence" in item:
                if not isinstance(item["confidence"], (int, float)) or not 0 <= item["confidence"] <= 1:
                    warnings.append(f"第{i+1}条：confidence 应为0.0-1.0之间的数值")
    
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
            for err in errors:
                print_error(err)
        if warnings:
            for warn in warnings:
                print_warning(warn)
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
            for err in errors:
                print_error(err)
        if warnings:
            for warn in warnings:
                print_warning(warn)
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
