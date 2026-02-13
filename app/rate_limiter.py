from __future__ import annotations

import time
from collections import defaultdict, deque
from typing import Deque, Dict

from fastapi import HTTPException, Request, status

from app.config import get_settings

settings = get_settings()


class RateLimiter:
    def __init__(self, max_requests_per_minute: int) -> None:
        self.max_requests = max_requests_per_minute
        self.window_seconds = 60
        self.requests: Dict[str, Deque[float]] = defaultdict(deque)

    def check(self, key: str) -> None:
        now = time.time()
        window_start = now - self.window_seconds
        q = self.requests[key]

        while q and q[0] < window_start:
            q.popleft()

        if len(q) >= self.max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests, please try again later.",
            )

        q.append(now)


rate_limiter = RateLimiter(max_requests_per_minute=settings.rate_limit_requests_per_minute)


async def limit_requests(request: Request) -> None:
    client_ip = request.client.host if request.client else "unknown"
    key = f"{client_ip}:{request.url.path}"
    rate_limiter.check(key)