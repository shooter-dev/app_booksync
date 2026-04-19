import asyncio

import pytest

from booksync.services import StreamChunk, StreamingService


def test_stream_chunk_has_id_and_content():
    chunk = StreamChunk(id=1, content="hello")
    assert chunk.id == 1
    assert chunk.content == "hello"


@pytest.mark.asyncio
async def test_streaming_service_yields_expected_chunks():
    service = StreamingService(source=["a", "b", "c"], delay=0)
    received = [chunk async for chunk in service.stream()]
    assert [c.content for c in received] == ["a", "b", "c"]
    assert [c.id for c in received] == [0, 1, 2]


@pytest.mark.asyncio
async def test_streaming_service_can_be_stopped():
    service = StreamingService(source=["a", "b", "c", "d"], delay=0.01)

    received: list[StreamChunk] = []

    async def consume():
        async for chunk in service.stream():
            received.append(chunk)
            if len(received) == 2:
                service.stop()

    await asyncio.wait_for(consume(), timeout=1.0)
    assert len(received) == 2
