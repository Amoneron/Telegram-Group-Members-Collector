#!/usr/bin/env python3
import asyncio
import time


class RateLimiter:
    def __init__(self, delay: float = 0.5):
        self.delay = delay
        self.last_request = 0

    async def wait(self):
        current_time = time.time()
        time_since_last = current_time - self.last_request

        if time_since_last < self.delay:
            await asyncio.sleep(self.delay - time_since_last)

        self.last_request = time.time()

    def reset(self):
        self.last_request = 0
