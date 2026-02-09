import React from 'react'

import { ActionRenderPropsNoArgs } from '@copilotkit/react-core'

export const GetTimeResult: React.FC<ActionRenderPropsNoArgs> = ({ args, result }) => {
  return (
    <div className='mt-4 rounded-lg border border-gray-300 bg-white p-4 shadow-sm'>
      <p className='text-gray-500'>{`Called the get_time API for ${JSON.stringify(args)}`}</p>
      <p className='mt-2 text-green-600'>Current time is: {result}</p>
    </div>
  )
}
