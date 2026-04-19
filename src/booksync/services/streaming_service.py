import asyncio
from collections.abc import AsyncIterator, Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class StreamChunk:
    id: int
    content: str


class StreamingService:
    """Produces `StreamChunk`s asynchronously.

    Kept free of Qt so it can be unit-tested without a GUI. A real
    implementation would read from a socket, HTTP SSE, or a file tail.
    """

    def __init__(self, source: Iterable[str], delay: float = 0.05) -> None:
        self._source = list(source)
        self._delay = delay
        self._stopped = False

    def stop(self) -> None:
        self._stopped = True

    async def stream(self) -> AsyncIterator[StreamChunk]:
        self._stopped = False
        for idx, item in enumerate(self._source):
            if self._stopped:
                return
            if self._delay:
                await asyncio.sleep(self._delay)
            if self._stopped:
                return
            yield StreamChunk(id=idx, content=item)
