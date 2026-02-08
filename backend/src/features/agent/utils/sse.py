import json

SSE_MEDIA_TYPE = "text/event-stream"


def sse_headers() -> dict[str, str]:
    return {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
    }


def encode_sse_event(event: dict) -> bytes:
    data = json.dumps(event, separators=(",", ":"))
    return f"data: {data}\n\n".encode()
