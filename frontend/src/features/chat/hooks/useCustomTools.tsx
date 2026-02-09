'use client'

import { useFrontendTool, useHumanInTheLoop, useRenderToolCall } from '@copilotkit/react-core'

import { DateSelector } from '../components/DateSelector'
import { GetTimeResult } from '../components/GetTimeResult'

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

  useHumanInTheLoop({
    name: 'selectDate',
    description: 'Let the user select a date from a calendar.',
    parameters: [
      {
        name: 'minDate',
        type: 'string',
        description: 'The minimum selectable date in YYYY-MM-DD format.',
        required: false,
      },
      {
        name: 'maxDate',
        type: 'string',
        description: 'The maximum selectable date in YYYY-MM-DD format.',
        required: false,
      },
    ],
    render: ({ args, status, respond, result }) => {
      if (status === 'executing' && respond) {
        return (
          <DateSelector
            minDate={args.minDate}
            maxDate={args.maxDate}
            onDateSelect={(date) => respond({ selectedDate: date })}
          />
        )
      }
      if (status === 'complete' && result) {
        return <div className='p-2 text-sm text-gray-600'>{result.selectedDate}</div>
      }

      return <div />
    },
  })
}
