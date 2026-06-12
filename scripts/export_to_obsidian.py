#!/usr/bin/env python3
"""
结直肠癌知识库 - Obsidian导出脚本
将数据转换为Obsidian格式，支持双链和标签
"""

import json
from pathlib import Path
import os

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
EXPORT_DIR = BASE_DIR / "obsidian-export"


def export_guideline_to_obsidian():
    """导出指南摘要到Obsidian格式"""
    guidelines_dir = DATA_DIR / "guidelines"
    export_guidelines_dir = EXPORT_DIR / "指南摘要"
    export_guidelines_dir.mkdir(parents=True, exist_ok=True)
    
    for md_file in guidelines_dir.rglob("*.md"):
        # 读取文件
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 转换为Obsidian格式（确保有双链）
        # 在标题行添加双链
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            # 在二级标题后添加相关笔记链接
            if line.startswith('## ') and '更新' in line:
                title = line.replace('## ', '').strip()
                new_lines.append(line)
                new_lines.append(f"\n[[相关{title}讨论]]")
            else:
                new_lines.append(line)
        
        # 在文件末尾添加标签（如果frontmatter中没有）
        if 'tags:' not in content:
            new_lines.append('\n\n---\n')
            new_lines.append('#结肠癌 #指南 #CSCO\n')
        
        # 保存
        relative_path = md_file.relative_to(guidelines_dir)
        export_path = export_guidelines_dir / relative_path
        export_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(export_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print(f"✅ 导出指南：{relative_path}")


def export_relations_to_obsidian():
    """导出知识图谱关系到Obsidian格式"""
    relations_file = DATA_DIR / "knowledge-graph" / "relations.json"
    export_dir = EXPORT_DIR / "知识图谱"
    export_dir.mkdir(parents=True, exist_ok=True)
    
    if not relations_file.exists():
        print("⚠️  未找到relations.json，跳过知识图谱导出")
        return
    
    with open(relations_file, 'r', encoding='utf-8') as f:
        relations = json.load(f)
    
    # 按知识主体分组，兼容当前 head/relation/tail 与早期 subject/predicate/object。
    subjects = {}
    for rel in relations:
        subject = rel.get('head') or rel.get('subject') or '未知'
        if subject not in subjects:
            subjects[subject] = []
        subjects[subject].append(rel)
    
    for subject, rels in subjects.items():
        # 生成文件名（Obsidian兼容）
        safe_name = subject.replace('/', '-').replace('\\', '-')
        file_path = export_dir / f"{safe_name}.md"
        
        # 生成内容
        content = f"---\ntitle: {subject}\ntype: knowledge_node\ntags: [知识图谱]\n---\n\n"
        content += f"# {subject}\n\n"
        content += "## 相关知识\n\n"
        
        for rel in rels:
            predicate = rel.get('relation') or rel.get('predicate') or ''
            obj = rel.get('tail') or rel.get('object') or ''
            evidence = rel.get('evidence') or rel.get('evidence_level') or ''
            source = rel.get('source', '')
            
            content += f"- **{predicate}**：[[{obj}]]（{evidence}，来源：{source}）\n"
        
        content += f"\n## 双链\n"
        content += f"[[{subject}-详情]]\n"
        
        # 保存
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 导出知识节点：{subject}")
    
    print(f"\n📊 共导出 {len(subjects)} 个知识节点")


def export_drugs_to_obsidian():
    """导出药物知识到Obsidian格式"""
    drugs_dir = DATA_DIR / "drugs"
    export_dir = EXPORT_DIR / "药物知识"
    export_dir.mkdir(parents=True, exist_ok=True)
    
    if not drugs_dir.exists():
        print("⚠️  未找到drugs目录，跳过药物知识导出")
        return
    
    for json_file in drugs_dir.glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            drugs = json.load(f)
        
        for drug in drugs:
            name = drug.get('name', '未知药物')
            safe_name = name.replace('/', '-').replace('\\', '-')
            file_path = export_dir / f"{safe_name}.md"
            
            # 生成Obsidian格式
            content = f"""---
title: {name}
english_name: {drug.get('english_name', '')}
type: {drug.get('type', '')}
tags: [药物, {drug.get('type', '')}]
---

# {name}

**英文名**：{drug.get('english_name', '')}

## 适应症

{drug.get('indication', '')}

## 剂量与用法

{drug.get('dosage', '')}

## 常见不良反应

{chr(10).join(['- ' + ae for ae in drug.get('common_adverse_events', [])])}

## 证据等级

{drug.get('evidence_level', '')}（来源：{drug.get('source', '')}）

## 相关链接

[[{drug.get('type', '')}药物列表]]
"""
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 导出药物：{name}")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("结直肠癌知识库 - 导出到Obsidian")
    print("="*60 + "\n")
    
    # 1. 导出指南摘要
    print("📚 导出指南摘要...")
    export_guideline_to_obsidian()
    
    # 2. 导出知识图谱
    print("\n🧬 导出知识图谱...")
    export_relations_to_obsidian()
    
    # 3. 导出药物知识
    print("\n💊 导出药物知识...")
    export_drugs_to_obsidian()
    
    print("\n" + "="*60)
    print(f"✅ 导出完成！文件保存在：{EXPORT_DIR}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
