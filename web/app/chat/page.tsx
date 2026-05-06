"use client"

import { useState, useEffect, useRef, Suspense } from 'react'
import { useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle } from '@/app/components/card'
import { Button } from '@/app/components/button'
import { ModelSelector } from '@/app/components/model-selector'
import { MessageCircle, Send, Loader2, BookOpen, ExternalLink, ChevronRight, ArrowLeft, Sparkles, Shield } from 'lucide-react'
import { type KnowledgeTriplet, getHead } from '@/lib/knowledge'

interface Message {
  role: 'user' | 'assistant'
  content: string
  sources?: KnowledgeTriplet[]
  suggestions?: string[]
  model?: string
  knowledgeUsed?: boolean
}

function ChatContent() {
  const searchParams = useSearchParams()
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)
  const [showSuggestions, setShowSuggestions] = useState(true)
  const [modelConfigured, setModelConfigured] = useState(false)
  const [currentModel, setCurrentModel] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const initialQuestion = searchParams.get('question')

  useEffect(() => {
    // 检查是否已配置模型
    const saved = localStorage.getItem('crc_model_config')
    if (saved) {
      try {
        const config = JSON.parse(saved)
        if (config.optionId && config.apiKey) {
          setModelConfigured(true)
          setCurrentModel(config.optionId)
        }
      } catch (e) {
        console.error('Failed to load config:', e)
      }
    }
  }, [])

  useEffect(() => {
    if (initialQuestion) {
      setInput(initialQuestion)
      setShowSuggestions(false)
      handleSubmit(initialQuestion)
    }
  }, [initialQuestion])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleModelSelect = (optionId: string, apiKey: string) => {
    if (optionId && apiKey) {
      setModelConfigured(true)
      setCurrentModel(optionId)
    } else {
      setModelConfigured(false)
      setCurrentModel('')
    }
  }

  const handleSubmit = async (text?: string) => {
    const query = text || input
    if (!query.trim()) return

    if (!modelConfigured) {
      // 如果未配置模型，使用本地知识库
      const userMessage: Message = { role: 'user', content: query }
      setMessages(prev => [...prev, userMessage])
      setInput('')
      setLoading(true)

      try {
        // 调用本地知识库
        const response = await fetch('/data/knowledge.json')
        const kb = await response.json()

        // 简单的关键词匹配
        const results = searchLocalKB(query, kb)
        const answer = formatLocalAnswer(query, results)

        const assistantMessage: Message = {
          role: 'assistant',
          content: answer,
          sources: results.slice(0, 3),
          suggestions: generateLocalSuggestions(query),
          model: '本地知识库',
          knowledgeUsed: results.length > 0
        }
        setMessages(prev => [...prev, assistantMessage])
      } catch (error) {
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: '知识库加载失败，请稍后再试。',
          model: '本地知识库'
        }])
      } finally {
        setLoading(false)
        setShowSuggestions(false)
      }
      return
    }

    // 使用大模型
    const userMessage: Message = { role: 'user', content: query }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)
    setShowSuggestions(false)

    try {
      const saved = JSON.parse(localStorage.getItem('crc_model_config') || '{}')

      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: query,
          modelOptionId: saved.optionId,
          apiKey: saved.apiKey,
          messages: messages.filter(m => m.role === 'user' || m.role === 'assistant').map(m => ({
            role: m.role,
            content: m.content
          }))
        })
      })

      const result = await response.json()

      if (!response.ok) {
        throw new Error(result.error || '服务暂时不可用')
      }

      const assistantMessage: Message = {
        role: 'assistant',
        content: result.answer,
        sources: result.sources,
        suggestions: result.suggestions,
        model: result.model,
        knowledgeUsed: result.knowledgeUsed
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error: any) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `抱歉，${error.message || '服务暂时不可用'}。请稍后再试。`,
        model: currentModel
      }])
    } finally {
      setLoading(false)
    }
  }

  // 本地知识库搜索
  function searchLocalKB(query: string, kb: KnowledgeTriplet[]): KnowledgeTriplet[] {
    const queryLower = query.toLowerCase()
    const keywords = queryLower.split(/\s+/).filter(k => k.length > 1)

    return kb
      .map(item => {
        const head = (item.head || item.subject || '').toLowerCase()
        const tail = (item.tail || item.object || '').toLowerCase()
        const relation = (item.relation || item.predicate || '').toLowerCase()

        let score = 0
        for (const kw of keywords) {
          if (head.includes(kw)) score += 3
          if (tail.includes(kw)) score += 2
          if (relation.includes(kw)) score += 1
        }

        return { item, score }
      })
      .filter(r => r.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 5)
      .map(r => r.item)
  }

  function formatLocalAnswer(query: string, results: KnowledgeTriplet[]): string {
    if (results.length === 0) {
      return '抱歉，我在知识库中没有找到与您问题相关的信息。\n\n建议：\n- 请尝试更具体的关键词\n- 咨询专业医生获取个性化建议'
    }

    let answer = `根据知识库检索，我找到以下相关信息：\n\n`

    const bySubject = new Map<string, KnowledgeTriplet[]>()
    for (const r of results) {
      const head = r.head || r.subject || '相关信息'
      if (!bySubject.has(head)) {
        bySubject.set(head, [])
      }
      bySubject.get(head)!.push(r)
    }

    for (const [subject, items] of bySubject) {
      answer += `📌 **${subject}**\n`
      for (const item of items.slice(0, 2)) {
        const relation = item.relation || item.predicate || ''
        const tail = item.tail || item.object || ''
        if (relation && tail) {
          answer += `- ${relation}：${tail}\n`
        }
      }
      answer += '\n'
    }

    answer += '---\n⚠️ 以上内容仅供参考，请咨询专业医生获取诊疗建议。'

    return answer
  }

  function generateLocalSuggestions(query: string): string[] {
    const q = query.toLowerCase()
    if (q.includes('化疗') || q.includes('治疗')) {
      return ['术后需要化疗吗？', '靶向治疗适合哪些人？', '治疗期间饮食注意']
    }
    if (q.includes('手术')) {
      return ['保肛手术条件？', '腹腔镜vs开放手术', '术后恢复要点']
    }
    return ['还有其他问题吗？', '详细了解治疗方案', '咨询具体症状']
  }

  const suggestions = [
    'II期结肠癌需要化疗吗？',
    '直肠癌放化疗方案有哪些？',
    '哪些基因突变影响靶向药选择？',
    '结直肠癌术后随访怎么安排？',
    'LARS综合征如何治疗？',
    '造口还纳的最佳时机？'
  ]

  return (
    <>
      {messages.length === 0 ? (
        <div className="flex-1 flex flex-col items-center justify-center">
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <MessageCircle className="w-8 h-8 text-blue-600" />
            </div>
            <h2 className="text-2xl font-bold mb-2">您好，我是CRC医学助手</h2>
            <p className="text-gray-600">基于CSCO、NCCN等权威指南，为您解答结直肠癌相关问题</p>

            {!modelConfigured && (
              <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg max-w-md mx-auto">
                <div className="flex items-center gap-2 text-yellow-800 mb-2">
                  <Sparkles className="w-5 h-5" />
                  <span className="font-medium">解锁更强大的AI能力</span>
                </div>
                <p className="text-sm text-yellow-700 mb-3">
                  点击右上角「选择模型」，配置您的API Key，即可使用DeepSeek、GPT-4o等大模型进行更智能的问答。
                </p>
                <p className="text-xs text-yellow-600">
                  💡 当前使用本地知识库直接检索
                </p>
              </div>
            )}
          </div>

          {showSuggestions && (
            <div className="w-full max-w-2xl">
              <p className="text-sm text-gray-500 mb-3">试试这些问题：</p>
              <div className="flex flex-wrap gap-2 justify-center">
                {suggestions.map((q, i) => (
                  <Button
                    key={i}
                    variant="outline"
                    size="sm"
                    onClick={() => handleSubmit(q)}
                    className="text-left"
                  >
                    <ChevronRight className="w-4 h-4 mr-1" />
                    {q}
                  </Button>
                ))}
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="flex-1 overflow-y-auto space-y-6 mb-4">
          {messages.map((msg, index) => (
            <div key={index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[80%] ${msg.role === 'user' ? 'order-2' : 'order-1'}`}>
                <Card className={msg.role === 'user' ? 'bg-blue-600 text-white' : ''}>
                  <CardContent className="p-4">
                    {msg.role === 'assistant' ? (
                      <div className="prose prose-sm max-w-none">
                        {/* 模型标识 */}
                        {msg.model && (
                          <div className="flex items-center gap-2 text-xs text-gray-500 mb-3 pb-2 border-b">
                            <Sparkles className="w-3 h-3" />
                            <span>由 {msg.model} 生成</span>
                            {msg.knowledgeUsed && (
                              <>
                                <span>•</span>
                                <BookOpen className="w-3 h-3" />
                                <span>参考知识库</span>
                              </>
                            )}
                          </div>
                        )}

                        <div className="whitespace-pre-wrap">{msg.content}</div>

                        {msg.sources && msg.sources.length > 0 && (
                          <div className="mt-4 pt-4 border-t">
                            <p className="text-xs text-gray-500 mb-2 flex items-center gap-1">
                              <BookOpen className="w-4 h-4" />
                              参考来源
                            </p>
                            <div className="space-y-2">
                              {msg.sources.slice(0, 3).map((s, i) => (
                                <div key={i} className="text-xs bg-gray-50 p-2 rounded">
                                  <span className="font-medium text-blue-600">{getHead(s)}</span>
                                  <span className="text-gray-500"> - {s.source}</span>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}

                        {msg.suggestions && msg.suggestions.length > 0 && (
                          <div className="mt-4">
                            <p className="text-xs text-gray-500 mb-2">您还可以问：</p>
                            <div className="flex flex-wrap gap-2">
                              {msg.suggestions.map((s, i) => (
                                <Button
                                  key={i}
                                  variant="ghost"
                                  size="sm"
                                  onClick={() => handleSubmit(s)}
                                  className="text-xs h-auto py-1"
                                >
                                  {s}
                                </Button>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    ) : (
                      <span>{msg.content}</span>
                    )}
                  </CardContent>
                </Card>
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center gap-2 text-gray-500">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>正在分析{modelConfigured ? '...' : '知识库...'}</span>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      )}

      {/* Input */}
      <div className="border-t bg-white p-4 rounded-t-xl">
        <form onSubmit={(e) => { e.preventDefault(); handleSubmit(); }} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="请输入您的问题..."
            className="flex-1 px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
          />
          <Button type="submit" disabled={loading || !input.trim()}>
            <Send className="w-4 h-4" />
            <span className="ml-2 hidden sm:inline">发送</span>
          </Button>
        </form>
        <div className="flex items-center justify-between mt-2">
          <p className="text-xs text-gray-400">
            ⚠️ 回答仅供参考，请咨询专业医生获取诊疗建议
          </p>
          {modelConfigured && (
            <div className="flex items-center gap-1 text-xs text-green-600">
              <Sparkles className="w-3 h-3" />
              <span>AI增强模式</span>
            </div>
          )}
        </div>
      </div>
    </>
  )
}

export default function ChatPage() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/">
              <Button variant="ghost" size="icon">
                <ArrowLeft className="w-5 h-5" />
              </Button>
            </Link>
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <MessageCircle className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="font-semibold">智能问答</h1>
                <p className="text-xs text-gray-500">基于3,253条权威医学知识</p>
              </div>
            </div>
          </div>
          <ModelSelector onSelect={() => {}} />
        </div>
      </header>

      {/* Chat Area */}
      <main className="flex-1 max-w-4xl mx-auto w-full px-4 py-6 flex flex-col">
        <Suspense fallback={
          <div className="flex-1 flex items-center justify-center">
            <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
          </div>
        }>
          <ChatContent />
        </Suspense>
      </main>

      {/* Footer Disclaimer */}
      <div className="bg-white border-t py-3">
        <div className="max-w-4xl mx-auto px-4">
          <div className="flex items-center gap-2 text-xs text-gray-500 justify-center">
            <Shield className="w-4 h-4" />
            <span>本系统仅供医学参考，不构成诊疗建议。复杂病情请咨询专业医生。</span>
          </div>
        </div>
      </div>
    </div>
  )
}
