# _obsidian-export_

本目录包含Obsidian格式的导出数据，可以直接导入到您的Obsidian Vault。

## 使用方法

### 方式一：直接复制文件到Vault

```bash
# 复制整个 obsidian-export 目录到您的 Vault
cp -r obsidian-export/* /path/to/your/obsidian-vault/
```

### 方式二：符号链接（推荐，自动同步）

```bash
# 创建符号链接，实现自动同步
ln -s /path/to/colorectal-cancer-kb/obsidian-export/* /path/to/your/obsidian-vault/
```

## 目录结构

```
obsidian-export/
├── 指南摘要/           # 指南摘要笔记
├── 知识图谱/           # 知识图谱笔记
├── 药物知识/           # 药物知识笔记
└── 临床试验/           # 临床试验数据
```

## 笔记模板

所有笔记均包含Obsidian frontmatter，支持：
- 双链 `[[笔记名]]`
- 标签 `#标签名`
- Dataview 查询（可选）

## 自动更新

当 `data/` 目录中的数据更新时，运行以下脚本自动更新Obsidian导出：

```bash
python scripts/export_to_obsidian.py
```

---

**维护方式**: 随知识库数据批次同步更新  
**最后更新**: 2026-05-07
