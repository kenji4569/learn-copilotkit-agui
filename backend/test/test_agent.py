from unittest import TestCase

from src.features.agent.utils.sse import encode_sse_event


class TestAgent(TestCase):
    def test_encode_sse_event(self):
        event = {
            "type": "CUSTOM",
            "name": "test",
            "value": {"message": "Hello"},
        }
        encoded = encode_sse_event(event)
        expected = (
            b'data: {"type":"CUSTOM","name":"test","value":{"message":"Hello"}}\n\n'
        )
        self.assertEqual(encoded, expected)
