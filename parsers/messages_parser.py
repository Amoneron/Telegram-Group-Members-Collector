#!/usr/bin/env python3
import asyncio
import signal
from typing import Dict, Any, List
from datetime import datetime, timedelta
from telethon.errors import FloodWaitError

from .base import BaseParser
from utils.rate_limiter import RateLimiter
from utils.progress import ProgressTracker
from config import RATE_LIMIT_DELAY


class MessagesParser(BaseParser):
    def __init__(self, client, chat_id):
        super().__init__(client, chat_id)
        self.rate_limiter = RateLimiter(RATE_LIMIT_DELAY)
        self.interrupted = False

    async def parse(self, days: int = 7, **kwargs) -> List[Dict[str, Any]]:
        chat = await self.client.get_entity(self.chat_id)

        print(f"\nParsing messages for: {getattr(chat, 'title', 'Chat')}")
        print(f"Chat ID: {self.chat_id}")
        print(f"Time period: last {days} days")
        print("-" * 50)

        participants = []
        start_date = datetime.now() - timedelta(days=days)
        end_date = datetime.now()

        total_messages = await self._estimate_total_messages(chat, start_date, end_date)
        progress = ProgressTracker(
            total=total_messages,
            desc=f"Scanning messages (last {days} days)"
        )

        message_count = 0
        unique_users = 0

        # Set up signal handler for graceful shutdown
        def signal_handler(signum, frame):
            self.interrupted = True
            print("\n\nReceived interrupt signal. Saving data...")
            progress.set_description("Saving data before exit...")

        signal.signal(signal.SIGINT, signal_handler)

        try:
            async for message in self.client.iter_messages(
                chat,
                limit=None
            ):
                if self.interrupted:
                    break

                await self.rate_limiter.wait()

                # Check if message is within our date range
                if message.date.replace(tzinfo=None) < start_date:
                    break  # Stop iteration as we've gone past our date range

                message_count += 1
                progress.update(1)

                if message.sender_id and not self.is_user_processed(message.sender_id):
                    try:
                        user = await message.get_sender()

                        if user and hasattr(user, 'id'):
                            user_data = await self.extract_user_data(user)

                            if user_data:
                                user_data['extracted_at'] = datetime.now().isoformat()
                                user_data['first_message_date'] = message.date.isoformat()
                                user_data['extraction_method'] = 'message'

                                participants.append(user_data)
                                self.mark_user_processed(user.id)
                                unique_users += 1

                                progress.set_description(
                                    f"Found {unique_users} unique users from {message_count} messages"
                                )

                    except FloodWaitError as e:
                        print(f"\nRate limit hit. Waiting {e.seconds} seconds...")
                        await asyncio.sleep(e.seconds)
                    except Exception:
                        continue

                if message_count % 100 == 0:
                    await asyncio.sleep(0.1)

        finally:
            progress.close()

        print(f"\nMessages scanned: {message_count}")
        print(f"Unique users found: {len(participants)}")
        return participants

    async def _estimate_total_messages(self, chat, start_date, end_date) -> int:
        try:
            count = 0
            async for message in self.client.iter_messages(chat, limit=1000):
                message_date = message.date.replace(tzinfo=None)
                if message_date < start_date:
                    break
                if message_date <= end_date:
                    count += 1

            return max(count, 10)  # Return at least 10 for progress bar
        except Exception:
            return 100
