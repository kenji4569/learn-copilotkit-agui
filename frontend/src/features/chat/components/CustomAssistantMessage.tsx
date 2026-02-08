import { AssistantMessage, AssistantMessageProps } from '@copilotkit/react-ui'

export const CustomAssistantMessage = (props: AssistantMessageProps) => {
  return (
    <AssistantMessage
      {...props}
      onRegenerate={() => {
        alert('Currently disabled')
      }}
      onThumbsUp={undefined}
      onThumbsDown={undefined}
    />
  )
}
