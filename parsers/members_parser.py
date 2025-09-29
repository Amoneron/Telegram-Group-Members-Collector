#!/usr/bin/env python3
import asyncio
import signal
from typing import Dict, Any, List
from datetime import datetime
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.errors import FloodWaitError

from .base import BaseParser
from utils.rate_limiter import RateLimiter
from utils.progress import ProgressTracker
from config import BATCH_SIZE, RATE_LIMIT_DELAY


class MembersListParser(BaseParser):
    def __init__(self, client, chat_id):
        super().__init__(client, chat_id)
        self.rate_limiter = RateLimiter(RATE_LIMIT_DELAY)
        self.interrupted = False

    async def parse(self, **kwargs) -> List[Dict[str, Any]]:
        chat = await self.client.get_entity(self.chat_id)

        print(f"\nParsing members list for: {chat.title}")
        print(f"Chat ID: {self.chat_id}")
        print("-" * 50)

        participants = []
        offset = 0

        total_count = await self._get_total_count(chat)
        progress = ProgressTracker(total=total_count, desc="Fetching members")

        # Set up signal handler for graceful shutdown
        def signal_handler(signum, frame):
            self.interrupted = True
            print("\n\nReceived interrupt signal. Saving data...")
            progress.set_description("Saving data before exit...")

        signal.signal(signal.SIGINT, signal_handler)

        try:
            while True:
                if self.interrupted:
                    break
                await self.rate_limiter.wait()

                try:
                    result = await self.client(GetParticipantsRequest(
                        chat,
                        ChannelParticipantsSearch(''),
                        offset,
                        BATCH_SIZE,
                        hash=0
                    ))
                except FloodWaitError as e:
                    print(f"\nRate limit hit. Waiting {e.seconds} seconds...")
                    await asyncio.sleep(e.seconds)
                    continue

                if not result.users:
                    break

                for user in result.users:
                    if not self.is_user_processed(user.id):
                        user_data = await self.extract_user_data(user)
                        if user_data:
                            user_data['extracted_at'] = datetime.now().isoformat()
                            participants.append(user_data)
                            self.mark_user_processed(user.id)

                            progress.update(1)
                            progress.set_description(
                                f"Processing @{user.username or 'no_username'}"
                            )

                if len(result.users) < BATCH_SIZE:
                    break

                offset += BATCH_SIZE

        finally:
            progress.close()

        print(f"\nTotal unique members found: {len(participants)}")
        return participants

    async def _get_total_count(self, chat) -> int:
        try:
            result = await self.client(GetParticipantsRequest(
                chat,
                ChannelParticipantsSearch(''),
                0,
                1,
                hash=0
            ))
            return result.count
        except Exception:
            return 0
