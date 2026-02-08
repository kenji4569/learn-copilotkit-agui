'use client'

import { useRenderToolCall } from '@copilotkit/react-core'
import { CopilotChat } from '@copilotkit/react-ui'

import { CustomAssistantMessage } from './components/CustomAssistantMessage'
import { GetTimeResult } from './components/RenderGetTimeToolCall'
import { useCustomPrompt } from './hooks/useCustomPrompt'

export const Chat: React.FC = () => {
  useRenderToolCall({
    name: 'get_time',
    render: (props) => {
      if (props.status !== 'complete') {
        return <div>Calling get_time API...</div>
      }

      return <GetTimeResult {...props} />
    },
  })

  const { prompt } = useCustomPrompt()

  return (
    <CopilotChat
      className='h-screen pb-8'
      labels={{
        title: 'Hello Copilotkit and AG-UI',
        initial: 'Hello. How can I help you?',
        placeholder: prompt?.placeholder ?? 'Type your message...',
      }}
      suggestions={prompt?.suggestions}
      AssistantMessage={CustomAssistantMessage}
    />
  )
}
