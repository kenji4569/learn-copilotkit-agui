import datetime
import logging
import time
import uuid

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from .utils.sse import SSE_MEDIA_TYPE, encode_sse_event, sse_headers

router = APIRouter()


@router.post("/agent")
async def agent_post(request: Request) -> StreamingResponse:
    payload = await request.json()

    logging.info(f"Received payload: {payload}")

    thread_id = payload.get("threadId") or f"thread-{uuid.uuid4().hex[:8]}"
    run_id = payload.get("runId") or f"run-{uuid.uuid4().hex[:8]}"
    msg_id = f"msg-{uuid.uuid4().hex[:8]}"
    tool_id = f"tool-{uuid.uuid4().hex[:8]}"

    async def event_stream():
        yield encode_sse_event(
            {"type": "RUN_STARTED", "threadId": thread_id, "runId": run_id}
        )
        yield encode_sse_event(
            {"type": "TEXT_MESSAGE_START", "messageId": msg_id, "role": "assistant"}
        )
        yield encode_sse_event(
            {"type": "TEXT_MESSAGE_CONTENT", "messageId": msg_id, "delta": "Hello"}
        )
        yield encode_sse_event({"type": "TEXT_MESSAGE_END", "messageId": msg_id})

        yield encode_sse_event(
            {
                "type": "TOOL_CALL_START",
                "toolCallId": tool_id,
                "toolCallName": "get_time",
            }
        )
        yield encode_sse_event(
            {
                "type": "TOOL_CALL_ARGS",
                "toolCallId": tool_id,
                "delta": '{"timezone":"Asia/Tokyo"}',
            }
        )
        time.sleep(0.5)  # Simulate delay
        yield encode_sse_event({"type": "TOOL_CALL_END", "toolCallId": tool_id})

        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        yield encode_sse_event(
            {
                "type": "TOOL_CALL_RESULT",
                "toolCallId": tool_id,
                "messageId": msg_id,
                "content": now.strftime("%Y-%m-%d %H:%M:%S JST"),
                "role": "tool",
            }
        )

        msg_id2 = f"msg-{uuid.uuid4().hex[:8]}"
        yield encode_sse_event(
            {"type": "TEXT_MESSAGE_START", "messageId": msg_id2, "role": "assistant"}
        )
        yield encode_sse_event(
            {"type": "TEXT_MESSAGE_CONTENT", "messageId": msg_id2, "delta": "Now"}
        )
        time.sleep(0.5)  # Simulate delay
        yield encode_sse_event(
            {
                "type": "TEXT_MESSAGE_CONTENT",
                "messageId": msg_id2,
                "delta": " finished!",
            }
        )
        yield encode_sse_event({"type": "TEXT_MESSAGE_END", "messageId": msg_id2})

        yield encode_sse_event(
            {
                "type": "CUSTOM",
                "name": "set_prompt",
                "value": {
                    "suggestions": [
                        {"title": "Weather", "message": "Tell me the weather in Tokyo"},
                        {
                            "title": "Summary",
                            "message": "Summarize this conversation in 3 lines",
                        },
                    ],
                    "placeholder": "What would you like to do next?",
                },
            }
        )

        yield encode_sse_event(
            {
                "type": "RUN_FINISHED",
                "threadId": thread_id,
                "runId": run_id,
                "result": "",
            }
        )

    return StreamingResponse(
        event_stream(), media_type=SSE_MEDIA_TYPE, headers=sse_headers()
    )
