import { HttpAgent, MiddlewareFunction } from '@ag-ui/client'
import { CopilotRuntime, ExperimentalEmptyAdapter, copilotRuntimeNextJSAppRouterEndpoint } from '@copilotkit/runtime'

const AG_UI_URL = 'http://127.0.0.1:8000/agent'
const MAX_INPUT_MESSAGES = 10

const agent = new HttpAgent({ url: AG_UI_URL })

const limitMessages =
  (max: number): MiddlewareFunction =>
  (input, next) => {
    const messages = input.messages ?? []

    return next.run({
      ...input,
      messages: messages.slice(-max),
    })
  }
agent.use(limitMessages(MAX_INPUT_MESSAGES))

const runtime = new CopilotRuntime({
  // @ts-ignore
  agents: { default: agent },
})

const serviceAdapter = new ExperimentalEmptyAdapter()

export const POST = async (req: Request) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: '/api/copilotkit',
  })

  return handleRequest(req)
}
