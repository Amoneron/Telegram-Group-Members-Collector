#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from telethon import TelegramClient
from telethon.tl.types import User


class BaseParser(ABC):
    def __init__(self, client: TelegramClient, chat_id: int):
        self.client = client
        self.chat_id = chat_id
        self.processed_users = set()

    @abstractmethod
    async def parse(self, **kwargs) -> List[Dict[str, Any]]:
        pass

    async def extract_user_data(self, user: User) -> Dict[str, Any]:
        if not user:
            return None

        # Get full user info including 'about' field
        try:
            full_user = await self.client.get_entity(user.id)

            # Try to get full user details with about field
            from telethon.tl.functions.users import GetFullUserRequest
            try:
                user_full = await self.client(GetFullUserRequest(full_user))
                about = user_full.full_user.about if hasattr(user_full.full_user, 'about') else None
            except Exception:
                about = None
        except Exception:
            full_user = user
            about = None

        return {
            'id': full_user.id,
            'username': full_user.username,
            'first_name': full_user.first_name,
            'last_name': full_user.last_name,
            'phone': full_user.phone,
            'about': about,
            'is_bot': getattr(full_user, 'bot', False),
            'is_verified': getattr(full_user, 'verified', False),
            'is_restricted': getattr(full_user, 'restricted', False),
            'is_scam': getattr(full_user, 'scam', False),
            'is_fake': getattr(full_user, 'fake', False),
            'is_premium': getattr(full_user, 'premium', False),
            'is_support': getattr(full_user, 'support', False),
            'access_hash': full_user.access_hash,
            'status': str(full_user.status.__class__.__name__) if hasattr(full_user, 'status') and full_user.status else None,
            'photo_id': full_user.photo.photo_id if hasattr(full_user, 'photo') and full_user.photo else None,
            'lang_code': getattr(full_user, 'lang_code', None),
            'extracted_at': None
        }

    def is_user_processed(self, user_id: int) -> bool:
        return user_id in self.processed_users

    def mark_user_processed(self, user_id: int):
        self.processed_users.add(user_id)
