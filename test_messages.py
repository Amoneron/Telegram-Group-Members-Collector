#!/usr/bin/env python3
import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient
from config import API_ID, API_HASH, SESSION_NAME


async def test_messages():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    try:
        await client.connect()

        if not await client.is_user_authorized():
            print("Session not authorized")
            return

        chat_id = -1001358652190
        chat = await client.get_entity(chat_id)
        start_date = datetime.now() - timedelta(days=2)

        print("Testing messages for last 2 days")
        print(f"Start date: {start_date}")
        print(f"Chat: {chat.title}")

        count = 0
        unique_users = set()

        async for message in client.iter_messages(chat, limit=50):
            message_date = message.date.replace(tzinfo=None)
            print(f"Message {count}: {message_date}, sender: {message.sender_id}")

            if message_date < start_date:
                print("Reached old messages, stopping")
                break

            count += 1
            if message.sender_id:
                unique_users.add(message.sender_id)

        print(f"Found {count} messages from last 2 days")
        print(f"Unique senders: {len(unique_users)}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(test_messages())
