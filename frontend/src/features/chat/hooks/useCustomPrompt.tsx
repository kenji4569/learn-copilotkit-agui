'use client'
import { useEffect, useState } from 'react'

import { AgentSubscriber, useAgent } from '@copilotkit/react-core/v2'

type PromptSuggestion = {
  title: string
  message: string
}

type CustomPrompt = {
  suggestions: PromptSuggestion[]
  placeholder: string
}

export const useCustomPrompt = () => {
  const [prompt, setPrompt] = useState<CustomPrompt | null>(null)

  const { agent } = useAgent({ agentId: 'default' })
  useEffect(() => {
    const subscriber: AgentSubscriber = {
      onCustomEvent: ({ event }) => {
        if (event.name === 'set_prompt') {
          setPrompt(event.value)
        }
      },
    }
    const { unsubscribe } = agent.subscribe(subscriber)

    return () => unsubscribe()
  }, [agent])

  return { prompt }
}
