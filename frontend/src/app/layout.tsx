import type { Metadata } from 'next'
import { Geist, Geist_Mono } from 'next/font/google'
import Image from 'next/image'

import '@/app/globals.css'
import { AuthProvider } from '@/features/auth/AuthProvider'
import { Login } from '@/features/auth/Login'
import { SpotManager } from '@/features/spot/SpotManager'
import { CopilotKit } from '@copilotkit/react-core'
import '@copilotkit/react-ui/styles.css'

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
})

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
})

export const metadata: Metadata = {
  title: 'AG-UI + CopilotKit Minimal',
  description: 'Minimal CopilotKit client connected to a local AG-UI server.',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang='en'>
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        <div className='flex min-h-screen w-full flex-col md:flex-row'>
          <CopilotKit runtimeUrl='/api/copilotkit'>
            <AuthProvider>
              <aside className='w-full border-b border-gray-200 p-6 md:w-1/5 md:border-r md:border-b-0'>
                <div className='flex flex-col space-y-4'>
                  <a
                    href='https://github.com/kenji4569/learn-copilotkit-agui/'
                    target='_blank'
                    rel='noopener noreferrer'
                    className='flex items-center space-x-2'>
                    <Image aria-hidden src='/github.svg' alt='Github icon' width={16} height={16} />
                    <span>Repository</span>
                  </a>
                  <Login />
                  <SpotManager />
                </div>
              </aside>
              <main className='flex w-full flex-1 items-start justify-center'>
                <div className='h-full w-full max-w-2xl'>{children}</div>
              </main>
            </AuthProvider>
          </CopilotKit>
        </div>
      </body>
    </html>
  )
}
