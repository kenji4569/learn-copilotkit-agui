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

    last_message = payload.get("messages", [])[-1] or {}
    if last_message.get("role") == "user":
        content = last_message.get("content", "")
        if content == "Get time in Tokyo":
            event_stream = generate_event_stream_for_get_time(thread_id, run_id)
        elif content == "Say hello to someone":
            event_stream = generate_event_stream_for_say_hello(thread_id, run_id)
        else:
            event_stream = generate_event_stream_for_echo(thread_id, run_id, content)
    else:
        event_stream = generate_event_stream_for_empty(thread_id, run_id)

    return StreamingResponse(
        event_stream,
        media_type=SSE_MEDIA_TYPE,
        headers=sse_headers(),
    )


async def generate_event_stream_for_empty(thread_id, run_id):
    logging.info("Generating empty event stream")
    yield encode_sse_event(
        {"type": "RUN_STARTED", "threadId": thread_id, "runId": run_id}
    )
    yield encode_sse_event(
        {
            "type": "RUN_FINISHED",
            "threadId": thread_id,
            "runId": run_id,
            "result": "",
        }
    )


async def generate_event_stream_for_echo(thread_id, run_id, content):
    logging.info("Generating echo event stream")
    yield encode_sse_event(
        {"type": "RUN_STARTED", "threadId": thread_id, "runId": run_id}
    )

    msg_id = f"msg-{uuid.uuid4().hex[:8]}"
    yield encode_sse_event(
        {"type": "TEXT_MESSAGE_START", "messageId": msg_id, "role": "assistant"}
    )

    words = content.split(" ")
    for i, word in enumerate(words):
        yield encode_sse_event(
            {
                "type": "TEXT_MESSAGE_CONTENT",
                "messageId": msg_id,
                "delta": word + (" " if i < len(words) - 1 else ""),
            }
        )
        time.sleep(0.1)  # Simulate delay

    yield encode_sse_event({"type": "TEXT_MESSAGE_END", "messageId": msg_id})
    yield encode_sse_event(
        {
            "type": "RUN_FINISHED",
            "threadId": thread_id,
            "runId": run_id,
            "result": "",
        }
    )


async def generate_event_stream_for_get_time(thread_id, run_id):
    logging.info("Generating get_time event stream")
    yield encode_sse_event(
        {"type": "RUN_STARTED", "threadId": thread_id, "runId": run_id}
    )

    msg_id = f"msg-{uuid.uuid4().hex[:8]}"
    yield encode_sse_event(
        {"type": "TEXT_MESSAGE_START", "messageId": msg_id, "role": "assistant"}
    )
    yield encode_sse_event(
        {
            "type": "TEXT_MESSAGE_CONTENT",
            "messageId": msg_id,
            "delta": "Getting the current time in Tokyo",
        }
    )
    yield encode_sse_event({"type": "TEXT_MESSAGE_END", "messageId": msg_id})

    tool_id = f"tool-{uuid.uuid4().hex[:8]}"
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
        {
            "type": "TEXT_MESSAGE_START",
            "messageId": msg_id2,
            "role": "assistant",
        }
    )
    yield encode_sse_event(
        {
            "type": "TEXT_MESSAGE_CONTENT",
            "messageId": msg_id2,
            "delta": "Got the current time in Tokyo!",
        }
    )
    yield encode_sse_event({"type": "TEXT_MESSAGE_END", "messageId": msg_id2})

    yield encode_sse_event(
        {
            "type": "RUN_FINISHED",
            "threadId": thread_id,
            "runId": run_id,
            "result": "",
        }
    )


async def generate_event_stream_for_say_hello(thread_id, run_id):
    logging.info("Generating say_hello event stream")
    yield encode_sse_event(
        {"type": "RUN_STARTED", "threadId": thread_id, "runId": run_id}
    )

    tool_id = f"tool-{uuid.uuid4().hex[:8]}"
    yield encode_sse_event(
        {
            "type": "TOOL_CALL_START",
            "toolCallId": tool_id,
            "toolCallName": "sayHello",
        }
    )
    yield encode_sse_event(
        {
            "type": "TOOL_CALL_ARGS",
            "toolCallId": tool_id,
            "delta": '{"name":"guest"}',
        }
    )
    yield encode_sse_event({"type": "TOOL_CALL_END", "toolCallId": tool_id})

    yield encode_sse_event(
        {
            "type": "RUN_FINISHED",
            "threadId": thread_id,
            "runId": run_id,
            "result": "",
        }
    )
