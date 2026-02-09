import type { Metadata } from 'next'
import { Geist, Geist_Mono } from 'next/font/google'
import Image from 'next/image'

import '@/app/globals.css'
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
          <aside className='w-full border-b border-gray-200 p-6 md:w-1/5 md:border-r md:border-b-0'>
            <a
              href='https://github.com/kenji4569/learn-copilotkit-agui/'
              target='_blank'
              rel='noopener noreferrer'
              className='flex items-center space-x-2'>
              <Image aria-hidden src='/github.svg' alt='Github icon' width={16} height={16} />
              <span>Repository</span>
            </a>
          </aside>
          <main className='flex w-full flex-1 items-start justify-center'>
            <div className='h-full w-full max-w-2xl'>
              <CopilotKit runtimeUrl='/api/copilotkit'>{children}</CopilotKit>
            </div>
          </main>
        </div>
      </body>
    </html>
  )
}
