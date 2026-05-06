"use client"

import { useState, useEffect } from 'react'
import { Button } from './button'
import { MODEL_OPTIONS, type ModelOption } from '@/lib/models'
import { Settings, ChevronDown, Check, X, Key, Globe, Bot, Cpu, Monitor } from 'lucide-react'

interface ModelSelectorProps {
  onSelect: (optionId: string, apiKey: string) => void
  currentSelection?: string
}

export function ModelSelector({ onSelect, currentSelection }: ModelSelectorProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [selectedOption, setSelectedOption] = useState<ModelOption | null>(null)
  const [apiKey, setApiKey] = useState('')
  const [showApiInput, setShowApiInput] = useState(false)

  useEffect(() => {
    // 从本地存储加载保存的配置
    const saved = localStorage.getItem('crc_model_config')
    if (saved) {
      try {
        const config = JSON.parse(saved)
        setApiKey(config.apiKey || '')
        const option = MODEL_OPTIONS.find(o => o.id === config.optionId)
        if (option) setSelectedOption(option)
      } catch (e) {
        console.error('Failed to load saved config:', e)
      }
    }
  }, [])

  const handleSelectOption = (option: ModelOption) => {
    setSelectedOption(option)
    setShowApiInput(true)
  }

  const handleConfirm = () => {
    if (selectedOption && apiKey.trim()) {
      // 保存到本地存储
      localStorage.setItem('crc_model_config', JSON.stringify({
        optionId: selectedOption.id,
        apiKey: apiKey.trim()
      }))
      onSelect(selectedOption.id, apiKey.trim())
      setIsOpen(false)
      setShowApiInput(false)
    }
  }

  const handleClear = () => {
    localStorage.removeItem('crc_model_config')
    setSelectedOption(null)
    setApiKey('')
    onSelect('', '')
  }

  const getIcon = (provider: string) => {
    switch (provider) {
      case 'deepseek': return <Globe className="w-5 h-5" />
      case 'openai': return <Bot className="w-5 h-5" />
      case 'anthropic': return <Cpu className="w-5 h-5" />
      case 'local': return <Monitor className="w-5 h-5" />
      default: return <Bot className="w-5 h-5" />
    }
  }

  return (
    <div className="relative">
      <Button
        variant="outline"
        size="sm"
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2"
      >
        <Settings className="w-4 h-4" />
        <span className="hidden sm:inline">
          {selectedOption ? `已选择: ${selectedOption.name}` : '选择模型'}
        </span>
        <ChevronDown className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </Button>

      {isOpen && (
        <div className="absolute right-0 top-full mt-2 w-80 bg-white rounded-lg shadow-xl border p-4 z-50">
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-semibold">选择AI模型</h3>
            <button onClick={() => setIsOpen(false)} className="text-gray-400 hover:text-gray-600">
              <X className="w-5 h-5" />
            </button>
          </div>

          {!showApiInput ? (
            <div className="space-y-2">
              <p className="text-sm text-gray-500 mb-3">
                选择您要使用的大模型平台：
              </p>
              {MODEL_OPTIONS.map(option => (
                <button
                  key={option.id}
                  onClick={() => handleSelectOption(option)}
                  className={`w-full p-3 rounded-lg border text-left transition-all hover:border-blue-500 hover:bg-blue-50 ${
                    selectedOption?.id === option.id ? 'border-blue-500 bg-blue-50' : ''
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{option.icon}</span>
                    <div>
                      <div className="font-medium">{option.name}</div>
                      <div className="text-xs text-gray-500">{option.description}</div>
                    </div>
                    {selectedOption?.id === option.id && (
                      <Check className="w-4 h-4 text-blue-600 ml-auto" />
                    )}
                  </div>
                </button>
              ))}
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                <span className="text-2xl">{selectedOption?.icon}</span>
                <div>
                  <div className="font-medium">{selectedOption?.name}</div>
                  <div className="text-xs text-gray-500">{selectedOption?.description}</div>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Key className="w-4 h-4 inline mr-1" />
                  API Key
                </label>
                <input
                  type="password"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder={`输入 ${selectedOption?.name} API Key`}
                  className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <p className="text-xs text-gray-500 mt-1">
                  API Key仅保存在本地浏览器中
                </p>
              </div>

              <div className="flex gap-2">
                <Button onClick={handleConfirm} className="flex-1" disabled={!apiKey.trim()}>
                  确认使用
                </Button>
                <Button variant="outline" onClick={() => setShowApiInput(false)}>
                  返回
                </Button>
              </div>
            </div>
          )}

          {selectedOption && (
            <button
              onClick={handleClear}
              className="w-full mt-3 text-sm text-red-600 hover:text-red-700"
            >
              清除配置
            </button>
          )}
        </div>
      )}
    </div>
  )
}
