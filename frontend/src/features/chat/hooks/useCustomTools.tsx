'use client'

import { useFrontendTool, useRenderToolCall } from '@copilotkit/react-core'

import { GetTimeResult } from '../components/RenderGetTimeToolCall'

export const useCustomTools = () => {
  useRenderToolCall({
    name: 'get_time',
    render: (props) => {
      if (props.status !== 'complete') {
        return <div>Calling get_time API...</div>
      }

      return <GetTimeResult {...props} />
    },
  })

  useFrontendTool({
    name: 'sayHello',
    description: 'Say hello to someone.',
    parameters: [
      {
        name: 'name',
        type: 'string',
        description: 'name of the person to greet',
        required: true,
      },
    ],
    handler({ name }) {
      const greetedAt = new Date()
      alert(`Hello, ${name}!`)

      return { greetedAt }
    },
  })
}
