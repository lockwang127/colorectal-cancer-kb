import { NextRequest, NextResponse } from 'next/server'
import { searchKnowledge, type KnowledgeTriplet, getHead, getRelation, getTail } from '@/lib/knowledge'
import { callModel, getModelConfig, buildKnowledgeContext } from '@/lib/models'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { question, modelOptionId, apiKey, messages } = body

    if (!question) {
      return NextResponse.json({ error: '问题不能为空' }, { status: 400 })
    }

    if (!modelOptionId || !apiKey) {
      return NextResponse.json({ error: '请先选择模型并配置API Key' }, { status: 400 })
    }

    // 获取模型配置
    const modelConfig = getModelConfig(modelOptionId, apiKey)
    if (!modelConfig) {
      return NextResponse.json({ error: '无效的模型配置' }, { status: 400 })
    }

    // 搜索知识库
    const searchResults = await searchKnowledge(question, 10)
    const triplets = searchResults.map(r => r.triplet)

    // 构建知识上下文
    const knowledgeContext = buildKnowledgeContext(triplets, 10)

    // 构建消息历史
    const chatMessages = messages || []
    chatMessages.push({ role: 'user', content: question })

    // 调用大模型
    const answer = await callModel(modelConfig, chatMessages, knowledgeContext)

    // 生成建议问题
    const suggestions = generateSuggestions(question, triplets)

    return NextResponse.json({
      answer,
      sources: triplets.slice(0, 5),
      suggestions,
      knowledgeUsed: triplets.length > 0,
      model: modelConfig.name
    })
  } catch (error: any) {
    console.error('Chat API Error:', error)
    return NextResponse.json(
      { error: error.message || '服务暂时不可用' },
      { status: 500 }
    )
  }
}

function generateSuggestions(
  question: string,
  triplets: KnowledgeTriplet[]
): string[] {
  const suggestions: string[] = []
  const questionLower = question.toLowerCase()

  // 基于问题类型生成建议
  if (questionLower.includes('化疗') || questionLower.includes('治疗')) {
    suggestions.push(
      '结直肠癌化疗期间如何管理副作用？',
      '术后需要辅助化疗吗？',
      '靶向治疗适合哪些患者？'
    )
  } else if (questionLower.includes('手术')) {
    suggestions.push(
      '保肛手术的适应证是什么？',
      '腹腔镜和开放手术哪个更好？',
      '术后恢复期需要注意什么？'
    )
  } else if (questionLower.includes('基因') || questionLower.includes('突变')) {
    suggestions.push(
      'KRAS突变患者的治疗方案？',
      'BRAF突变预后如何？',
      '哪些基因检测是必需的？'
    )
  } else if (questionLower.includes('随访') || questionLower.includes('复查')) {
    suggestions.push(
      '术后随访应该做哪些检查？',
      '多久复查一次CEA？',
      '什么时候需要做肠镜复查？'
    )
  } else if (questionLower.includes('生存') || questionLower.includes('预后')) {
    suggestions.push(
      '各分期5年生存率是多少？',
      '影响预后的因素有哪些？',
      '早期和晚期预后差异？'
    )
  } else {
    // 默认建议
    suggestions.push(
      'LARS综合征如何改善？',
      '造口护理的注意事项？',
      '饮食上有什么禁忌？'
    )
  }

  return suggestions.slice(0, 3)
}
