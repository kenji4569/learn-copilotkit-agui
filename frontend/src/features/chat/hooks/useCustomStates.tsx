'use client'

import { useContext } from 'react'

import { AuthContext } from '@/features/auth/AuthProvider'
import { useCoAgentStateRender, useCopilotReadable } from '@copilotkit/react-core'

import { SpotList } from '../components/SpotList'

export type AgentState = {
  spots: string[]
}

export const useCustomStates = () => {
  useCoAgentStateRender<AgentState>({
    name: 'default', // MUST match the agent name in CopilotRuntime
    render: ({ state }) => {
      if (!state.spots) {
        return null
      }

      return <SpotList spots={state.spots} />
    },
  })

  const me = useContext(AuthContext)
  // Define Copilot readable state
  useCopilotReadable({
    description: 'Current user',
    value: me,
  })
}
