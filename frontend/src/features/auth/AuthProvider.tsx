'use client'

import { Dispatch, FC, SetStateAction, createContext, useContext, useState } from 'react'

export const AuthContext = createContext<string | null>('')
export const SetAuthContext = createContext<Dispatch<SetStateAction<string | null>>>(() => undefined)

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [me, setMe] = useState<string | null>(null)

  return (
    <AuthContext.Provider value={me}>
      <SetAuthContext.Provider value={setMe}>{children}</SetAuthContext.Provider>
    </AuthContext.Provider>
  )
}
