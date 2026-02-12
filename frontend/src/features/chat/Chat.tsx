'use client'

import { CopilotChat } from '@copilotkit/react-ui'

import { CustomAssistantMessage } from './components/CustomAssistantMessage'
import { useCustomStates } from './hooks/useCustomStates'
import { useCustomTools } from './hooks/useCustomTools'

export const Chat: React.FC = () => {
  useCustomTools()
  useCustomStates()

  const suggestions = [
    {
      title: 'Say something',
      message:
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    },
    { title: 'Get Time', message: 'Get time in Tokyo' },
    { title: 'Say Hello', message: 'Say hello to me' },
    { title: 'Select Date', message: 'Select a date from a calendar' },
    { title: 'Recommend Spots', message: 'Recommend tourist spots in Tokyo' },
    { title: 'Get Price', message: 'Get price of the tour' },
  ]

  return (
    <CopilotChat
      className='h-screen pb-8'
      labels={{
        title: 'Hello Copilotkit and AG-UI',
        initial: 'Hello. How can I help you?',
        placeholder: 'Type your message...',
      }}
      suggestions={suggestions}
      AssistantMessage={CustomAssistantMessage}
    />
  )
}
