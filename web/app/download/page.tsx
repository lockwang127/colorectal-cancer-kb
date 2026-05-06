"use client"

import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/app/components/card'
import { Button } from '@/app/components/button'
import { ArrowLeft, Download, FileJson, Zap, Database, Users } from 'lucide-react'

// GitHub Logo SVG
function GitHubLogo({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
    </svg>
  )
}

export default function DownloadPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-4">
          <Link href="/">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="w-5 h-5" />
            </Button>
          </Link>
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <Download className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="font-semibold">下载知识库</h1>
              <p className="text-xs text-gray-500">开源免费 · 持续更新</p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* Hero */}
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4">获取完整知识库</h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            知识库采用 JSON 格式，便于二次开发和 AI 应用。
            所有内容遵循 CC BY-NC-SA 4.0 协议，可免费用于非商业目的。
          </p>
        </div>

        {/* Download Options */}
        <div className="grid md:grid-cols-2 gap-6 mb-12">
          {/* JSON Download */}
          <Card className="border-2 border-blue-200">
            <CardHeader>
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <FileJson className="w-6 h-6 text-blue-600" />
              </div>
              <CardTitle>JSON 知识库</CardTitle>
              <CardDescription>
                结构化三元组数据，适合 AI 应用和二次开发
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-500">文件大小</span>
                  <span>约 500KB</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">知识条目</span>
                  <span>567 条</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">格式</span>
                  <span>JSON Lines</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">版本</span>
                  <span>v1.0.0</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">更新日期</span>
                  <span>2026-05-06</span>
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex-col gap-2">
              <Button className="w-full gap-2">
                <Download className="w-4 h-4" />
                下载 JSON
              </Button>
              <Button variant="outline" className="w-full gap-2">
                <Database className="w-4 h-4" />
                复制数据接口
              </Button>
            </CardFooter>
          </Card>

          {/* GitHub */}
          <Card>
            <CardHeader>
              <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mb-4">
                <GitHubLogo className="w-6 h-6 text-gray-700" />
              </div>
              <CardTitle>GitHub 仓库</CardTitle>
              <CardDescription>
                完整的开源项目，包含源码、数据和文档
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-500">仓库地址</span>
                  <span className="text-blue-600">lockwang127/colorectal-cancer-kb</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">星标</span>
                  <span>欢迎 Star ⭐</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">协议</span>
                  <span>CC BY-NC-SA 4.0</span>
                </div>
              </div>
              <div className="mt-4 p-3 bg-gray-50 rounded-lg text-xs">
                <code>git clone https://github.com/lockwang127/colorectal-cancer-kb.git</code>
              </div>
            </CardContent>
            <CardFooter>
              <Button variant="outline" className="w-full gap-2">
                <GitHubLogo className="w-4 h-4" />
                访问 GitHub
              </Button>
            </CardFooter>
          </Card>
        </div>

        {/* Features */}
        <Card className="mb-12">
          <CardHeader>
            <CardTitle>知识库特点</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="flex gap-3">
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Database className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <h4 className="font-medium mb-1">结构化数据</h4>
                  <p className="text-sm text-gray-500">
                    JSON 格式，包含实体、关系、属性，便于机器读取
                  </p>
                </div>
              </div>
              <div className="flex gap-3">
                <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Zap className="w-5 h-5 text-green-600" />
                </div>
                <div>
                  <h4 className="font-medium mb-1">AI-Ready</h4>
                  <p className="text-sm text-gray-500">
                    支持 RAG、知识图谱构建、模型训练等多种 AI 应用
                  </p>
                </div>
              </div>
              <div className="flex gap-3">
                <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Users className="w-5 h-5 text-purple-600" />
                </div>
                <div>
                  <h4 className="font-medium mb-1">社区共建</h4>
                  <p className="text-sm text-gray-500">
                    欢迎提交 Issue 和 Pull Request，共同完善知识库
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Usage Examples */}
        <Card>
          <CardHeader>
            <CardTitle>使用示例</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h4 className="font-medium mb-2 text-sm">Python 加载知识库</h4>
                <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg text-sm overflow-x-auto">
{`import json

# 加载知识库
with open('relations.json', 'r', encoding='utf-8') as f:
    relations = json.load(f)

print(f"知识条目: {len(relations)}")

# 查找相关知识
for item in relations:
    if '结肠癌' in item['subject'] and '化疗' in item['predicate']:
        print(f"- {item['subject']}: {item['object']}")`}
                </pre>
              </div>

              <div>
                <h4 className="font-medium mb-2 text-sm">JavaScript 加载知识库</h4>
                <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg text-sm overflow-x-auto">
{`// 加载知识库
const fs = require('fs');
const relations = JSON.parse(
  fs.readFileSync('relations.json', 'utf-8')
);

console.log(\`知识条目: \${relations.length}\`);

// 查找相关知识
const filtered = relations.filter(
  r => r.subject.includes('结肠癌') && r.predicate.includes('化疗')
);
console.log(filtered);`}
                </pre>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Disclaimer */}
        <div className="mt-8 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <p className="text-sm text-yellow-800">
            <strong>⚠️ 免责声明：</strong>
            本知识库内容仅供医学科普和学术研究使用，不构成临床诊疗建议。
            临床决策请务必咨询专业医生，结合患者具体情况制定治疗方案。
            知识库内容可能存在滞后，请以最新指南为准。
          </p>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t py-8 mt-12">
        <div className="max-w-4xl mx-auto px-4 text-center text-sm text-gray-500">
          <p>CRC MedQA - 结直肠癌通用知识库</p>
          <p className="mt-1">© 2026 四川大学华西医院胃肠外科</p>
        </div>
      </footer>
    </div>
  )
}
