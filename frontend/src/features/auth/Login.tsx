'use client'

import { useContext } from 'react'

import { AuthContext, SetAuthContext } from './AuthProvider'

export const Login: React.FC = () => {
  const me = useContext(AuthContext)
  const setMe = useContext(SetAuthContext)

  return (
    <div>
      {me ? (
        <div>{`Hello, ${me}`}</div>
      ) : (
        <button
          className='cursor-pointer rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600'
          onClick={() => {
            setMe('John Doe')
          }}>
          Login
        </button>
      )}
    </div>
  )
}
