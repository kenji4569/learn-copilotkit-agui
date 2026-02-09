# Frontend with CopilotKit

Next.js frontend with CopilotKit integration for AI-powered chat interface.

*This is originated from following Next.js Starters*
- [**Next.js 16 Starter Core**](https://github.com/SiddharthaMaity/nextjs-16-starter-core)
- [**Next.js 16 Starter with Tailwind CSS**](https://github.com/SiddharthaMaity/nextjs-16-starter-tailwind)
- [**Next.js 16 Starter with Shadcn UI**](https://github.com/siddharthamaity/nextjs-16-starter-shadcn)

## Getting Started

First, install dependencies and run the development server:

```bash
pnpm install
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Add shadcn UI Components

When you need to add a shadcn component, run a command like this:

```bash
pnpm dlx shadcn@latest add calendar
```



## Directory Structure

```
frontend/
├── src/
│   ├── app/                      # Next.js App Router
│   │   ├── api/
│   │   │   └── copilotkit/
│   │   │       └── route.ts      # **CopilotKit API endpoint**
│   │   ├── layout.tsx            # Root layout
│   │   └── page.tsx              # Home page
│   └── features/
│       └── chat/                 # Chat feature
│           ├── components/
│           ├── hooks/
│           └── Chat.tsx          # **Main chat component**
...
```

[`src/app/api/copilotkit/route.ts`](src/app/api/copilotkit/route.ts) is the CopilotKit API endpoint which interacts with the backend based on AG-UI.
[`src/features/chat/Chat.tsx`](src/features/chat/Chat.tsx) is the main chat component utilizing CopilotKit for the AI chat interface.

## Tech Stack

- **Next.js 16** - React framework with App Router and Turbopack
- **React 19** - UI library
- **Tailwind CSS** - Utility-first CSS framework
- **CopilotKit** - AI copilot framework for chat interface

### Development Tools
- **ESLint** - Code linting
- **Prettier** - Code formatting
- **TypeScript ESLint** - TypeScript linting
