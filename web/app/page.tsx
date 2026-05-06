"use client"

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/app/components/card'
import { Button } from '@/app/components/button'
import { MessageCircle, BookOpen, Download, Zap, Shield, Users, Database, ChevronRight } from 'lucide-react'
import { getKnowledgeStats } from '@/lib/knowledge'

export default function Home() {
  const [stats, setStats] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getKnowledgeStats().then(s => {
      setStats(s)
      setLoading(false)
    })
  }, [])

  const features = [
    {
      icon: <MessageCircle className="w-6 h-6" />,
      title: '智能问答',
      description: '基于权威指南的自然语言问答，获得专业的结直肠癌医学科普信息'
    },
    {
      icon: <BookOpen className="w-6 h-6" />,
      title: '知识浏览',
      description: '结构化浏览557+条医学知识，覆盖分期、治疗、基因等7大领域'
    },
    {
      icon: <Download className="w-6 h-6" />,
      title: '离线下载',
      description: '一键下载完整知识库，JSON格式便于二次开发和AI应用'
    },
    {
      icon: <Shield className="w-6 h-6" />,
      title: '权威来源',
      description: '所有知识均标注CSCO/NCCN/ESMO/AJCC等权威来源，可追溯可验证'
    }
  ]

  const hotQuestions = [
    'II期结肠癌需要化疗吗？',
    '直肠癌新辅助放化疗方案',
    'MSI-H/dMMR患者可以用免疫治疗吗？',
    '结直肠癌肝转移还能手术吗？',
    '造口术后如何护理？',
    'LARS综合征有哪些表现？'
  ]

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">CRC</span>
            </div>
            <span className="font-semibold text-lg">CRC MedQA</span>
          </div>
          <nav className="hidden md:flex items-center gap-6">
            <Link href="/chat" className="text-sm hover:text-blue-600">智能问答</Link>
            <Link href="/knowledge" className="text-sm hover:text-blue-600">知识库</Link>
            <Link href="/download" className="text-sm hover:text-blue-600">下载</Link>
          </nav>
          <Button size="sm">开始使用</Button>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-6xl mx-auto px-4 py-20 text-center">
        <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm mb-6">
          <Zap className="w-4 h-4" />
          基于557+条权威医学知识
        </div>
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
          您的结直肠癌
          <br />
          <span className="text-blue-600">专业医学问答助手</span>
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-8">
          基于CSCO、NCCN、ESMO等权威指南，为您提供专业的结直肠癌科普知识。
          无论您是患者、家属还是医学学习者，都能在这里找到可靠的答案。
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/chat">
            <Button size="lg" className="gap-2">
              <MessageCircle className="w-5 h-5" />
              开始提问
            </Button>
          </Link>
          <Link href="/knowledge">
            <Button size="lg" variant="outline" className="gap-2">
              <BookOpen className="w-5 h-5" />
              浏览知识库
            </Button>
          </Link>
        </div>

        {/* Stats */}
        <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card className="text-center">
            <CardContent className="pt-6">
              <div className="text-3xl font-bold text-blue-600">
                {loading ? '...' : (stats?.total || 0)}
              </div>
              <div className="text-sm text-gray-500">知识条目</div>
            </CardContent>
          </Card>
          <Card className="text-center">
            <CardContent className="pt-6">
              <div className="text-3xl font-bold text-blue-600">7</div>
              <div className="text-sm text-gray-500">知识领域</div>
            </CardContent>
          </Card>
          <Card className="text-center">
            <CardContent className="pt-6">
              <div className="text-3xl font-bold text-blue-600">50+</div>
              <div className="text-sm text-gray-500">权威来源</div>
            </CardContent>
          </Card>
          <Card className="text-center">
            <CardContent className="pt-6">
              <div className="text-3xl font-bold text-blue-600">7×24</div>
              <div className="text-sm text-gray-500">持续服务</div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Features */}
      <section className="max-w-6xl mx-auto px-4 py-16">
        <h2 className="text-2xl font-bold text-center mb-12">核心功能</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center text-blue-600 mb-4">
                  {feature.icon}
                </div>
                <CardTitle>{feature.title}</CardTitle>
                <CardDescription>{feature.description}</CardDescription>
              </CardHeader>
            </Card>
          ))}
        </div>
      </section>

      {/* Hot Questions */}
      <section className="bg-gray-50 py-16">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-2xl font-bold text-center mb-8">热门问题</h2>
          <div className="flex flex-wrap justify-center gap-3">
            {hotQuestions.map((q, index) => (
              <Link key={index} href={`/chat?question=${encodeURIComponent(q)}`}>
                <Button variant="outline" className="gap-2 h-auto py-2 whitespace-normal text-left">
                  <ChevronRight className="w-4 h-4 flex-shrink-0" />
                  {q}
                </Button>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Sources */}
      <section className="max-w-6xl mx-auto px-4 py-16">
        <h2 className="text-2xl font-bold text-center mb-8">知识来源</h2>
        <Card>
          <CardContent className="pt-6">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
              <div>
                <div className="text-lg font-semibold text-blue-600">CSCO 2024</div>
                <div className="text-sm text-gray-500">中国临床肿瘤学会指南</div>
              </div>
              <div>
                <div className="text-lg font-semibold text-blue-600">NCCN 2024</div>
                <div className="text-sm text-gray-500">美国国立综合癌症网络</div>
              </div>
              <div>
                <div className="text-lg font-semibold text-blue-600">ESMO</div>
                <div className="text-sm text-gray-500">欧洲肿瘤内科学会</div>
              </div>
              <div>
                <div className="text-lg font-semibold text-blue-600">AJCC</div>
                <div className="text-sm text-gray-500">美国癌症分期联合委员会</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* CTA */}
      <section className="bg-blue-600 py-16">
        <div className="max-w-4xl mx-auto px-4 text-center text-white">
          <h2 className="text-3xl font-bold mb-4">立即开始使用</h2>
          <p className="text-blue-100 mb-8">
            下载知识库或直接开始提问，获取专业的结直肠癌医学科普信息
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/chat">
              <Button size="lg" variant="outline" className="gap-2 bg-white">
                <MessageCircle className="w-5 h-5" />
                智能问答
              </Button>
            </Link>
            <Link href="/download">
              <Button size="lg" variant="outline" className="gap-2 bg-transparent border-white text-white hover:bg-white/10">
                <Download className="w-5 h-5" />
                下载知识库
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8">
        <div className="max-w-6xl mx-auto px-4 text-center text-sm text-gray-500">
          <p className="mb-2">
            CRC MedQA - 结直肠癌通用知识库
          </p>
          <p className="text-red-500 font-medium">
            ⚠️ 本产品仅供医学科普参考，不构成临床诊疗建议
          </p>
          <p className="mt-2">
            © 2026 四川大学华西医院胃肠外科 | 知识库采用 CC BY-NC-SA 4.0 协议
          </p>
        </div>
      </footer>
    </div>
  )
}
