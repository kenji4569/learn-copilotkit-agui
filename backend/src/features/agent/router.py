import datetime
import json
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
    thread_id = payload.get("threadId") or f"thread-{uuid.uuid4().hex[:8]}"
    run_id = payload.get("runId") or f"run-{uuid.uuid4().hex[:8]}"
    last_message = payload.get("messages", [])[-1] or {}
    context = payload.get("context", [])
    state = payload.get("state", [])

    logging.info(f"Received payload: {payload}")
    if last_message.get("role") == "user":
        content = last_message.get("content", "")
        if content == "Get time in Tokyo":
            event_stream = generate_event_stream_for_get_time(thread_id, run_id)
        elif content == "Say hello to me":
            name = _get_name_from_context(context)
            event_stream = generate_event_stream_for_say_hello(thread_id, run_id, name)
        elif content == "Select a date from a calendar":
            event_stream = generate_event_stream_for_select_date(thread_id, run_id)
        elif content == "Recommend tourist spots in Tokyo":
            event_stream = generate_event_stream_for_spots(
                thread_id,
                run_id,
            )
        elif content == "Get price of the tour":
            spots = state.get("spots", [])
            event_stream = generate_event_stream_for_pricing(thread_id, run_id, spots)
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
        time.sleep(0.02)  # Simulate delay

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
    time.sleep(0.2)  # Simulate delay
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


def _get_name_from_context(context: list):
    user_str = next(
        (c.get("value") for c in context if c.get("description") == "Current user"),
        None,
    )
    return (user_str and json.loads(user_str)) or "guest"


async def generate_event_stream_for_say_hello(thread_id, run_id, name):
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
            "delta": '{"name":"' + name + '"}',
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


async def generate_event_stream_for_select_date(thread_id, run_id):
    logging.info("Generating select_date event stream")
    yield encode_sse_event(
        {"type": "RUN_STARTED", "threadId": thread_id, "runId": run_id}
    )

    tool_id = f"tool-{uuid.uuid4().hex[:8]}"
    yield encode_sse_event(
        {
            "type": "TOOL_CALL_START",
            "toolCallId": tool_id,
            "toolCallName": "selectDate",
        }
    )

    minDate = datetime.date.today().isoformat()
    maxDate = (datetime.date.today() + datetime.timedelta(days=7)).isoformat()
    yield encode_sse_event(
        {
            "type": "TOOL_CALL_ARGS",
            "toolCallId": tool_id,
            "delta": '{"minDate":"' + minDate + '", "maxDate":"' + maxDate + '"}',
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


def generate_event_stream_for_spots(thread_id, run_id):
    logging.info("Generating recommend_tourist_spots event stream")
    yield encode_sse_event(
        {"type": "RUN_STARTED", "threadId": thread_id, "runId": run_id}
    )

    yield encode_sse_event(
        {
            "type": "STATE_SNAPSHOT",
            "snapshot": {"spots": []},
        }
    )
    time.sleep(0.5)  # Simulate delay
    yield encode_sse_event(
        {
            "type": "STATE_DELTA",
            "delta": [{"op": "add", "path": "/spots/-", "value": "Tokyo Tower"}],
        }
    )
    time.sleep(0.5)  # Simulate delay
    yield encode_sse_event(
        {
            "type": "STATE_DELTA",
            "delta": [{"op": "add", "path": "/spots/-", "value": "Senso-ji Temple"}],
        }
    )
    time.sleep(0.5)  # Simulate delay
    yield encode_sse_event(
        {
            "type": "STATE_DELTA",
            "delta": [{"op": "add", "path": "/spots/-", "value": "Skytree"}],
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


def generate_event_stream_for_pricing(thread_id, run_id, spots):
    logging.info("Generating get_pricing event stream")
    yield encode_sse_event(
        {"type": "RUN_STARTED", "threadId": thread_id, "runId": run_id}
    )

    price = 5000 * len(spots)
    msg_id = f"msg-{uuid.uuid4().hex[:8]}"
    yield encode_sse_event(
        {"type": "TEXT_MESSAGE_START", "messageId": msg_id, "role": "assistant"}
    )
    yield encode_sse_event(
        {
            "type": "TEXT_MESSAGE_CONTENT",
            "messageId": msg_id,
            "delta": f"The total price for the tour is {price} JPY.",
        }
    )
    yield encode_sse_event({"type": "TEXT_MESSAGE_END", "messageId": msg_id})

    yield encode_sse_event(
        {
            "type": "RUN_FINISHED",
            "threadId": thread_id,
            "runId": run_id,
            "result": "",
        }
    )
