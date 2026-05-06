"use client"

import { useState, useEffect, useRef, Suspense } from 'react'
import { useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle } from '@/app/components/card'
import { Button } from '@/app/components/button'
import { generateAnswer, type KnowledgeTriplet, getHead } from '@/lib/knowledge'
import { MessageCircle, Send, Loader2, BookOpen, ExternalLink, ChevronRight, ArrowLeft } from 'lucide-react'

interface Message {
  role: 'user' | 'assistant'
  content: string
  sources?: KnowledgeTriplet[]
  suggestions?: string[]
}

function ChatContent() {
  const searchParams = useSearchParams()
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)
  const [showSuggestions, setShowSuggestions] = useState(true)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const initialQuestion = searchParams.get('question')

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

  const handleSubmit = async (text?: string) => {
    const query = text || input
    if (!query.trim()) return

    const userMessage: Message = { role: 'user', content: query }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)
    setShowSuggestions(false)

    try {
      const result = await generateAnswer(query)
      const assistantMessage: Message = {
        role: 'assistant',
        content: result.answer,
        sources: result.sources,
        suggestions: result.suggestions
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      const errorMessage: Message = {
        role: 'assistant',
        content: '抱歉，服务暂时不可用。请稍后再试。',
        suggestions: ['结直肠癌治疗', '化疗方案', '术后随访']
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
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
                    <span>正在分析知识库...</span>
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
        <p className="text-xs text-gray-400 mt-2 text-center">
          ⚠️ 回答仅供参考，请咨询专业医生获取诊疗建议
        </p>
      </div>
    </>
  )
}

export default function ChatPage() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
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
              <MessageCircle className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="font-semibold">智能问答</h1>
              <p className="text-xs text-gray-500">基于567条权威医学知识</p>
            </div>
          </div>
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
    </div>
  )
}
