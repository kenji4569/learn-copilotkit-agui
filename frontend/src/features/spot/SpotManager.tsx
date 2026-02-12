'use client'
import { useCoAgent } from '@copilotkit/react-core'

import { AgentState } from '../chat/hooks/useCustomStates'

export const SpotManager: React.FC = () => {
  const { state, setState } = useCoAgent<AgentState>({
    name: 'default', // MUST match the agent name in CopilotRuntime
  })
  if (!state.spots) {
    return null
  }

  return (
    <div className='mt-4'>
      <h2 className='font-semibold'>Recommended Spots:</h2>
      {state.spots.map((spot) => (
        <div key={spot} className='text-sm text-gray-600'>
          {spot}
        </div>
      ))}
      <div>
        <button
          className='mt-2 cursor-pointer rounded bg-blue-500 px-3 py-1 text-sm text-white hover:bg-blue-600'
          onClick={() => {
            // Example of updating the agent state
            const newSpots = [...state.spots].slice(0, -1)
            setState({ spots: newSpots })
          }}>
          -
        </button>
      </div>
    </div>
  )
}
