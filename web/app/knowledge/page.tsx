"use client"

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/app/components/card'
import { Button } from '@/app/components/button'
import { loadKnowledgeBase, type KnowledgeTriplet, getHead, getRelation, getTail, getEvidence } from '@/lib/knowledge'
import { ArrowLeft, Search, Filter, BookOpen, Database, Tag, ChevronDown } from 'lucide-react'

const domains = [
  '全部', '系统治疗', '肛管癌', '阑尾肿瘤', '围手术期管理',
  '外科手术', '基因靶点', '病理·营养·预后', '分期系统',
  '造口·随访·筛查', 'LARS与并发症'
]

export default function KnowledgePage() {
  const [knowledge, setKnowledge] = useState<KnowledgeTriplet[]>([])
  const [filtered, setFiltered] = useState<KnowledgeTriplet[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [selectedDomain, setSelectedDomain] = useState('全部')
  const [showFilters, setShowFilters] = useState(false)

  useEffect(() => {
    loadKnowledgeBase().then(data => {
      setKnowledge(data)
      setFiltered(data)
      setLoading(false)
    })
  }, [])

  useEffect(() => {
    let result = knowledge

    if (selectedDomain !== '全部') {
      result = result.filter(k => k.domain === selectedDomain)
    }

    if (search.trim()) {
      const query = search.toLowerCase()
      result = result.filter(k =>
        getHead(k).toLowerCase().includes(query) ||
        getRelation(k).toLowerCase().includes(query) ||
        getTail(k).toLowerCase().includes(query)
      )
    }

    setFiltered(result)
  }, [search, selectedDomain, knowledge])

  const domainCounts = domains.slice(1).map(d => ({
    name: d,
    count: knowledge.filter(k => k.domain === d).length
  })).filter(d => d.count > 0)

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center gap-4">
          <Link href="/">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="w-5 h-5" />
            </Button>
          </Link>
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <BookOpen className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="font-semibold">知识库</h1>
              <p className="text-xs text-gray-500">{knowledge.length} 条医学知识</p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-6">
        {/* Search & Filter */}
        <div className="mb-6">
          <div className="flex gap-4 mb-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="搜索知识..."
                className="w-full pl-10 pr-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <Button variant="outline" onClick={() => setShowFilters(!showFilters)}>
              <Filter className="w-4 h-4 mr-2" />
              筛选
              <ChevronDown className="w-4 h-4 ml-2" />
            </Button>
          </div>

          {showFilters && (
            <Card className="mb-4">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm">知识领域</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {domains.map(domain => (
                    <Button
                      key={domain}
                      variant={selectedDomain === domain ? 'default' : 'outline'}
                      size="sm"
                      onClick={() => setSelectedDomain(domain)}
                    >
                      {domain}
                      {domain !== '全部' && (
                        <span className="ml-2 text-xs opacity-70">
                          {knowledge.filter(k => k.domain === domain).length}
                        </span>
                      )}
                    </Button>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <Card>
            <CardContent className="pt-6 text-center">
              <div className="text-2xl font-bold text-blue-600">{knowledge.length}</div>
              <div className="text-xs text-gray-500">知识总数</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6 text-center">
              <div className="text-2xl font-bold text-blue-600">{domainCounts.length}</div>
              <div className="text-xs text-gray-500">知识领域</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6 text-center">
              <div className="text-2xl font-bold text-blue-600">{filtered.length}</div>
              <div className="text-xs text-gray-500">当前显示</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6 text-center">
              <div className="text-2xl font-bold text-green-600">
                {Math.round(filtered.length / knowledge.length * 100)}%
              </div>
              <div className="text-xs text-gray-500">覆盖率</div>
            </CardContent>
          </Card>
        </div>

        {/* Domain Distribution */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="text-base">知识域分布</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {domainCounts.sort((a, b) => b.count - a.count).map(d => (
                <div key={d.name} className="flex items-center gap-3">
                  <span className="w-32 text-sm truncate">{d.name}</span>
                  <div className="flex-1 h-4 bg-gray-100 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-blue-600 rounded-full transition-all"
                      style={{ width: `${(d.count / knowledge.length) * 100}%` }}
                    />
                  </div>
                  <span className="w-12 text-sm text-gray-500 text-right">{d.count}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Knowledge List */}
        <Card>
          <CardHeader>
            <CardTitle>知识列表</CardTitle>
            <CardDescription>
              显示 {filtered.length} 条知识
              {selectedDomain !== '全部' && ` · ${selectedDomain}`}
            </CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center py-8 text-gray-500">加载中...</div>
            ) : filtered.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                未找到匹配的知识
              </div>
            ) : (
              <div className="space-y-4">
                {filtered.slice(0, 50).map((item, index) => (
                  <div key={index} className="border-b pb-4 last:border-0">
                    <div className="flex items-start gap-2 mb-2">
                      <span className="px-2 py-0.5 bg-blue-100 text-blue-700 text-xs rounded">
                        {item.domain || '未分类'}
                      </span>
                      <span className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">
                        {getEvidence(item)}
                      </span>
                    </div>
                    <h3 className="font-medium text-lg mb-1">{getHead(item)}</h3>
                    <p className="text-gray-600 text-sm mb-2">
                      <span className="text-blue-600">{getRelation(item)}</span>：{getTail(item)}
                    </p>
                    <div className="flex items-center gap-4 text-xs text-gray-400">
                      <span>来源：{item.source || '未知'}</span>
                      {item.confidence && (
                        <span>置信度：{(item.confidence * 100).toFixed(0)}%</span>
                      )}
                    </div>
                  </div>
                ))}
                {filtered.length > 50 && (
                  <div className="text-center pt-4">
                    <Button variant="outline">查看更多</Button>
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
