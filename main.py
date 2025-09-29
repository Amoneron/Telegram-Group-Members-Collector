#!/usr/bin/env python3
import argparse
import asyncio
import sys

from telethon import TelegramClient

from config import (
    API_ID, API_HASH, SESSION_NAME, RESULTS_DIR,
    SYSTEM_VERSION, DEVICE_MODEL, APP_VERSION, LANG_CODE
)
from parsers.members_parser import MembersListParser
from parsers.messages_parser import MessagesParser
from utils.data_export import DataExporter


async def auth_mode(client):
    print("Authorization mode")
    print("-" * 50)

    await client.start()
    print("Authorization completed successfully!")
    print("Now you can run the script with parsing parameters")


async def parse_members(client, chat_id):
    parser = MembersListParser(client, chat_id)
    members = await parser.parse()

    if members:
        exporter = DataExporter(RESULTS_DIR)
        chat_info = {
            'chat_id': chat_id,
            'mode': 'members_list'
        }
        filepath = exporter.save_batch_data(members, chat_info)
        print(f"\nData saved to: {filepath}")

    return members


async def parse_messages(client, chat_id, days):
    parser = MessagesParser(client, chat_id)
    members = await parser.parse(days=days)

    if members:
        exporter = DataExporter(RESULTS_DIR)
        chat_info = {
            'chat_id': chat_id,
            'mode': 'messages',
            'parameters': {'days': days}
        }
        filepath = exporter.save_batch_data(members, chat_info)
        print(f"\nData saved to: {filepath}")

    return members


async def main():
    parser = argparse.ArgumentParser(
        description='Telegram Group Members Collector',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Authorize (first time only)
  python main.py --auth

  # Parse members list
  python main.py -c -1001234567890 -m members

  # Parse from messages (last 30 days)
  python main.py -c -1001234567890 -m messages -d 30
        """
    )

    parser.add_argument('--auth', action='store_true',
                        help='Authorization mode (first time only)')
    parser.add_argument('-c', '--chat', type=int,
                        help='Chat ID (e.g., -1001234567890)')
    parser.add_argument('-m', '--mode', choices=['members', 'messages'],
                        help='Parsing mode: members list or messages')
    parser.add_argument('-d', '--days', type=int, default=7,
                        help='Number of days to scan messages (default: 7, for messages mode only)')

    args = parser.parse_args()

    client = TelegramClient(
        SESSION_NAME,
        API_ID,
        API_HASH,
        system_version=SYSTEM_VERSION,
        device_model=DEVICE_MODEL,
        app_version=APP_VERSION,
        lang_code=LANG_CODE
    )

    try:
        if args.auth:
            await auth_mode(client)
        elif args.chat and args.mode:
            await client.start()

            print("\n" + "-" * 60)
            print("Telegram Group Members Collector")
            print("=" * 60)
            print(f"Mode: {args.mode}")
            print(f"Chat ID: {args.chat}")

            if args.mode == 'members':
                await parse_members(client, args.chat)
            elif args.mode == 'messages':
                print(f"Days to scan: {args.days}")
                await parse_messages(client, args.chat, args.days)
        else:
            parser.print_help()
            sys.exit(1)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        await client.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
